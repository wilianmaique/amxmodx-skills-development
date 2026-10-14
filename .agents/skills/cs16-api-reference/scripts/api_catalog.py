#!/usr/bin/env python3
"""Read-only, source-backed discovery for the CS 1.6 / AMXX skill collection.

Uses only Python's standard library. This is a lexical reference index, not a
Pawn preprocessor or compiler. Conditional declarations and macro expressions
are retained without inventing their active branches or numeric values.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import fnmatch
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Iterable

SKILL_DIR = Path(__file__).resolve().parents[1]
PACK_DIR = SKILL_DIR.parent
SNAPSHOT_DIR = SKILL_DIR / "references" / "includes"
MANIFEST_PATH = SKILL_DIR / "references" / "manifest.json"
KINDS = ("native", "forward", "stock", "stock-variable", "enum", "constant", "hook", "member", "macro")


@dataclass(frozen=True)
class Symbol:
    name: str
    kind: str
    include: str
    line: int
    end_line: int
    doc_line: int
    signature: str
    enum: str = ""
    deprecated: bool = False
    implementation_end_line: int = 0


def mask_source(source: str) -> str:
    """Blank comments and literal contents while preserving offsets/newlines."""
    result = list(source)
    pos = 0
    state = "code"
    quote = ""
    while pos < len(source):
        char = source[pos]
        nxt = source[pos:pos + 2]
        if state == "code":
            if nxt == "//":
                result[pos:pos + 2] = "  "
                pos += 2
                state = "line"
                continue
            if nxt == "/*":
                result[pos:pos + 2] = "  "
                pos += 2
                state = "block"
                continue
            if char in ('"', "'"):
                quote = char
                state = "string"
        elif state == "line":
            if char == "\n":
                state = "code"
            else:
                result[pos] = " "
        elif state == "block":
            if nxt == "*/":
                result[pos:pos + 2] = "  "
                pos += 2
                state = "code"
                continue
            if char != "\n":
                result[pos] = " "
        else:
            # Pawn's default escape is ^. Backslash is a literal character in
            # these includes, including the valid character constant '\\'.
            if char == "^" and pos + 1 < len(source):
                if source[pos] != "\n":
                    result[pos] = " "
                if source[pos + 1] != "\n":
                    result[pos + 1] = " "
                pos += 2
                continue
            if char == quote:
                state = "code"
            elif char != "\n":
                result[pos] = " "
        pos += 1
    return "".join(result)


def line_number(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def matching_close(masked: str, opening: int, left: str, right: str) -> int:
    depth = 0
    for pos in range(opening, len(masked)):
        if masked[pos] == left:
            depth += 1
        elif masked[pos] == right:
            depth -= 1
            if depth == 0:
                return pos
    raise ValueError(f"Unclosed {left} at offset {opening}")


def documentation_start(lines: list[str], first_line: int) -> int:
    """Attach adjacent docs and deprecation pragmas, not earlier declarations."""
    pos = first_line - 2
    start = first_line
    while pos >= 0:
        stripped = lines[pos].strip()
        if not stripped:
            pos -= 1
            continue
        if stripped.startswith("#pragma deprecated"):
            start = pos + 1
            pos -= 1
            continue
        if stripped.endswith("*/") and ("/*" not in stripped or stripped.startswith("/*")):
            while pos >= 0:
                start = pos + 1
                if "/*" in lines[pos]:
                    pos -= 1
                    break
                pos -= 1
            continue
        if stripped.startswith("//"):
            start = pos + 1
            pos -= 1
            continue
        break
    return start


def make_symbol(source: str, lines: list[str], filename: str, name: str,
                kind: str, start: int, end: int, enum: str = "",
                implementation_end: int = 0) -> Symbol:
    first_line = line_number(source, start)
    last_line = line_number(source, end)
    doc_line = documentation_start(lines, first_line)
    documentation = "\n".join(lines[doc_line - 1:last_line])
    return Symbol(
        name=name, kind=kind, include=filename, line=first_line,
        end_line=last_line, doc_line=doc_line,
        signature=" ".join(source[start:end + 1].split()), enum=enum,
        deprecated=bool(re.search(r"@deprecated|#pragma deprecated|\bDeprecated\b|\bDEPRECATED\b", documentation)),
        implementation_end_line=line_number(source, implementation_end) if implementation_end else last_line,
    )


def parse_include(filename: str, source: str) -> list[Symbol]:
    masked = mask_source(source)
    lines = source.splitlines()
    symbols: list[Symbol] = []

    declaration = re.compile(
        r"^[ \t]*(native|forward|stock)[ \t]+"
        r"(?:(?:const|static)[ \t]+)*(?:\[[^\n\]]+\][ \t]*)?"
        r"(?:(?:[A-Za-z_]\w*|\{[^\n}]+\})[ \t]*:[ \t]*)?(?:\[[^\n\]]+\][ \t]*)?"
        r"([A-Za-z_]\w*|operator[^\s(]+)[ \t]*\(", re.M,
    )
    function_starts: set[int] = set()
    for match in declaration.finditer(masked):
        opening = masked.rfind("(", match.start(), match.end())
        close = matching_close(masked, opening, "(", ")")
        end = close
        next_pos = close + 1
        while next_pos < len(masked) and masked[next_pos].isspace():
            next_pos += 1
        implementation_end = end
        if next_pos < len(masked) and masked[next_pos] == "{":
            implementation_end = matching_close(masked, next_pos, "{", "}")
        elif match.group(1) in ("native", "forward"):
            semicolon = masked.find(";", next_pos)
            if semicolon >= 0:
                end = semicolon
                implementation_end = end
        elif masked.startswith("return", next_pos):
            semicolon = masked.find(";", next_pos)
            if semicolon >= 0:
                implementation_end = semicolon
        actual_start = match.start() + len(match.group(0)) - len(match.group(0).lstrip())
        symbols.append(make_symbol(source, lines, filename, match.group(2), match.group(1),
                                   actual_start, end, implementation_end=implementation_end))
        function_starts.add(match.start())

    variables = re.compile(
        r"^[ \t]*stock[ \t]+(?:(?:const|static)[ \t]+)*"
        r"(?:[A-Za-z_]\w*[ \t]*:[ \t]*)?([A-Za-z_]\w*)[ \t]*(?=[=;\[])", re.M,
    )
    for match in variables.finditer(masked):
        if match.start() in function_starts:
            continue
        end = masked.find(";", match.end())
        if end < 0:
            end = masked.find("\n", match.end())
        symbols.append(make_symbol(source, lines, filename, match.group(1), "stock-variable",
                                   match.start(), end))

    for match in re.finditer(r"^[ \t]*#define[ \t]+([A-Za-z_]\w*)", masked, re.M):
        end = source.find("\n", match.end())
        if end < 0:
            end = len(source)
        while source[match.start():end].rstrip().endswith("\\") and end < len(source):
            next_end = source.find("\n", end + 1)
            end = next_end if next_end >= 0 else len(source)
        definition = source[match.start():end]
        name_end = match.end()
        is_macro = name_end < len(masked) and masked[name_end] == "("
        symbols.append(make_symbol(source, lines, filename, match.group(1),
                                   "macro" if is_macro else "constant", match.start(), end - 1))

    enum_pattern = re.compile(r"\benum\b([^\n{;]*)(?:\n[ \t]*)?\{", re.M)
    for match in enum_pattern.finditer(masked):
        opening = masked.find("{", match.start(), match.end())
        closing = matching_close(masked, opening, "{", "}")
        head = match.group(1).strip()
        name_match = re.match(r"(?:[A-Za-z_]\w*\s*:\s*)?([A-Za-z_]\w*)", head)
        enum_name = name_match.group(1) if name_match else ""
        if enum_name:
            symbols.append(make_symbol(source, lines, filename, enum_name, "enum", match.start(), opening, implementation_end=closing))
        chunk_start = opening + 1
        depth = 0
        for pos in range(opening + 1, closing + 1):
            char = masked[pos]
            if char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
            if (char == "," and depth == 0) or pos == closing:
                chunk = masked[chunk_start:pos]
                # Ignore preprocessor lines embedded inside an enum.
                chunk = re.sub(r"(?m)^[ \t]*#[^\n]*", lambda m: " " * len(m.group()), chunk)
                entry = re.match(r"\s*(?:[A-Za-z_]\w*\s*:\s*)?([A-Za-z_]\w*)", chunk)
                if entry:
                    name = entry.group(1)
                    start = chunk_start + entry.start(1)
                    end = pos - 1
                    while end > start and source[end].isspace():
                        end -= 1
                    kind = "constant"
                    if name.startswith(("RG_", "RH_", "RC_", "Ham_", "FM_")):
                        kind = "hook"
                    elif name.startswith(("m_", "var_", "pm_", "ucmd_", "movevars_", "netadr_", "netchan_")):
                        kind = "member"
                    symbols.append(make_symbol(source, lines, filename, name, kind, start, end, enum_name))
                chunk_start = pos + 1

    # The same declaration can occur in alternate preprocessor branches.
    return sorted(symbols, key=lambda symbol: (symbol.line, symbol.kind, symbol.name))


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def ownership(manifest: dict) -> dict[str, str]:
    return {filename: skill for skill, names in manifest["owners"].items() for filename in names}


def source_directory(explicit: str | None) -> tuple[Path, str]:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_dir() or not any(path.glob("*.inc")):
            raise ValueError(f"Include directory has no .inc files: {path}")
        return path, "explicit project compiler includes"
    return SNAPSHOT_DIR, "bundled reference snapshot; use --include-dir for the project's compiler includes"


def load_sources(directory: Path, patterns: Iterable[str]) -> dict[str, str]:
    files = sorted(directory.glob("*.inc"), key=lambda path: path.name.casefold())
    if patterns:
        files = [path for path in files if any(fnmatch.fnmatchcase(path.name.casefold(), pattern.casefold()) for pattern in patterns)]
    # utf-8-sig removes a BOM; replacement decoding keeps older comment encodings readable.
    return {path.name: path.read_text(encoding="utf-8-sig", errors="replace") for path in files}


def print_symbol(symbol: Symbol, directory: Path, owners: dict, source: str,
                 implementation: bool) -> None:
    status = " [deprecated]" if symbol.deprecated else ""
    print(f"{symbol.name} ({symbol.kind}){status} | skill: {owners.get(symbol.include, 'unmapped')}")
    print(f"Source: {directory / symbol.include}:{symbol.line}")
    if symbol.enum:
        print(f"Enum: {symbol.enum} (expressions are not evaluated)")
    end = symbol.implementation_end_line if implementation else symbol.end_line
    for number, text in enumerate(source.splitlines()[symbol.doc_line - 1:end], symbol.doc_line):
        print(f"{number:>5}: {text}")
    print()


def validate_pack(manifest: dict) -> list[str]:
    problems: list[str] = []
    owned_files = [name for files in manifest["owners"].values() for name in files]
    duplicate_owners = [name for name, count in Counter(owned_files).items() if count != 1]
    if duplicate_owners:
        problems.append(f"Files have duplicate ownership: {duplicate_owners}")
    if set(owned_files) != set(manifest["files"]):
        problems.append("Manifest fingerprints and include ownership do not match")
    actual = {path.name for path in SNAPSHOT_DIR.glob("*.inc")}
    if actual != set(owned_files):
        problems.append(f"Snapshot coverage differs: missing={sorted(set(owned_files) - actual)}, extra={sorted(actual - set(owned_files))}")
    expected_skills = set(manifest["owners"]) | {"cs16-api-reference"}
    present_skills = {path.parent.name for path in PACK_DIR.glob("*/SKILL.md")}
    if present_skills != expected_skills:
        problems.append(f"Skill coverage differs: missing={sorted(expected_skills - present_skills)}, extra={sorted(present_skills - expected_skills)}")
    for name, fingerprint in manifest["files"].items():
        path = SNAPSHOT_DIR / name
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != fingerprint["sha256"]:
            problems.append(f"Changed snapshot fingerprint: {name}")
    for skill_name in sorted(expected_skills & present_skills):
        skill = PACK_DIR / skill_name / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match or not re.search(r"(?m)^name:\s*" + re.escape(skill_name) + r"\s*$", match.group(1)) or not re.search(r"(?m)^description:\s*\S", match.group(1)):
            problems.append(f"Invalid skill frontmatter: {skill_name}")
        metadata = skill.parent / "agents" / "openai.yaml"
        if not metadata.is_file() or "allow_implicit_invocation: false" in metadata.read_text(encoding="utf-8"):
            problems.append(f"Missing or explicitly disabled discovery metadata: {skill_name}")
        for name in manifest["owners"].get(skill_name, []):
            if name not in text:
                problems.append(f"SKILL.md does not identify owned include: {skill_name}/{name}")
    # Validate local resource links throughout authored Markdown.
    for document in PACK_DIR.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        for link in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", text):
            target = link.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            if not (document.parent / target).resolve().exists():
                problems.append(f"Broken local link: {document.relative_to(PACK_DIR)} -> {target}")
    return problems


def run(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("list", "find", "show", "raw", "coverage", "validate"))
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--include-dir", help="Exact include directory used by the target Pawn compiler; never merged with the snapshot")
    parser.add_argument("--include", action="append", default=[], help="Include filename/glob; repeat to filter")
    parser.add_argument("--kind", choices=KINDS)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--context", type=int, default=4)
    parser.add_argument("--docs", action="store_true", help="Also search adjacent documentation")
    parser.add_argument("--implementation", action="store_true", help="Show complete stock or enum bodies")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(arguments)
    if args.limit < 1 or args.context < 0:
        parser.error("--limit must be positive and --context cannot be negative")
    if args.command in ("find", "show", "raw") and not args.query:
        parser.error(f"{args.command} requires a query")
    manifest = load_manifest()
    owners = ownership(manifest)
    if args.command == "validate":
        problems = validate_pack(manifest)
        result = {"ok": not problems, "includes": len(manifest["files"]), "skills": len(manifest["owners"]) + 1, "problems": problems}
        print(json.dumps(result, indent=2) if args.json else "\n".join(problems) if problems else f"PASS: {result['skills']} skills, {result['includes']} fingerprinted includes, ownership, metadata and local links")
        return 1 if problems else 0
    directory, source_label = source_directory(args.include_dir)
    sources = load_sources(directory, args.include)
    if not sources:
        raise ValueError("No includes match the requested filters")
    if not args.json:
        print(f"Source set: {directory}\nPolicy: {source_label}\n")
    if args.command == "coverage":
        expected = set(owners)
        found = set(sources)
        changed = sorted(name for name in expected & found if hashlib.sha256((directory / name).read_bytes()).hexdigest() != manifest["files"].get(name, {}).get("sha256"))
        result = {"source_dir": str(directory), "expected": len(expected), "found": len(found),
                  "missing": sorted(expected - found), "unmapped": sorted(found - expected), "changed_since_snapshot": changed}
        print(json.dumps(result, indent=2))
        return 1 if result["missing"] or result["unmapped"] else 0
    # Raw source search must still work for a custom include with a syntax or
    # preprocessor construct that this lexical parser does not understand.
    symbols = [] if args.command == "raw" else [symbol for filename, source in sources.items() for symbol in parse_include(filename, source)]
    if args.command == "list":
        result = []
        for filename, source in sources.items():
            counts = Counter(symbol.kind for symbol in symbols if symbol.include == filename)
            record = {"include": filename, "skill": owners.get(filename, "unmapped"), "lines": len(source.splitlines()),
                      "symbols": sum(counts.values()), "kinds": dict(counts),
                      "includes": re.findall(r"(?m)^\s*#(?:try)?include\s+[<\"]([^>\"]+)[>\"]", source),
                      "module_pragmas": re.findall(r"(?m)^\s*#pragma\s+(?:reqlib|loadlib|library)\s+(\w+)", source)}
            result.append(record)
        if args.json:
            print(json.dumps({"source_dir": str(directory), "files": result}, indent=2))
        else:
            for record in result:
                print(f"{record['include']:<28} {record['lines']:>5} lines {record['symbols']:>4} symbols  {record['skill']}")
            print(f"\n{len(result)} includes; {len(symbols)} lexical symbol declarations (conditional duplicates retained)")
        return 0
    if args.command == "raw":
        matches = []
        for filename, source in sources.items():
            lines = source.splitlines()
            for number, line in enumerate(lines, 1):
                if args.query.casefold() in line.casefold():
                    start = max(1, number - args.context)
                    end = min(len(lines), number + args.context)
                    matches.append({"include": filename, "path": str(directory / filename), "line": number,
                                    "skill": owners.get(filename, "unmapped"), "start_line": start,
                                    "text": "\n".join(lines[start - 1:end])})
        if args.json:
            print(json.dumps({"source_dir": str(directory), "total": len(matches), "matches": matches[:args.limit]}, indent=2))
        else:
            for match in matches[:args.limit]:
                print(f"{match['path']}:{match['line']} | {match['skill']}")
                for number, line in enumerate(match["text"].splitlines(), match["start_line"]):
                    print(f"{number:>5}: {line}")
                print()
            print(f"{len(matches)} matches; showing {min(args.limit, len(matches))}")
        return 0 if matches else 1
    query = args.query.casefold()
    matches = []
    for symbol in symbols:
        if args.kind and symbol.kind != args.kind:
            continue
        is_match = symbol.name.casefold() == query if args.command == "show" else query in symbol.name.casefold()
        if args.docs and args.command == "find" and not is_match:
            doc = "\n".join(sources[symbol.include].splitlines()[symbol.doc_line - 1:symbol.end_line])
            is_match = query in doc.casefold()
        if is_match:
            matches.append(symbol)
    matches.sort(key=lambda symbol: (symbol.name.casefold() != query, not symbol.name.casefold().startswith(query), symbol.name.casefold(), symbol.include, symbol.line))
    if args.json:
        result = []
        for symbol in matches[:args.limit]:
            record = asdict(symbol)
            record["skill"] = owners.get(symbol.include, "unmapped")
            record["path"] = str(directory / symbol.include)
            if args.command == "show":
                end = symbol.implementation_end_line if args.implementation else symbol.end_line
                record["source"] = "\n".join(sources[symbol.include].splitlines()[symbol.doc_line - 1:end])
            result.append(record)
        print(json.dumps({"source_dir": str(directory), "total": len(matches), "symbols": result}, indent=2))
    elif args.command == "show":
        for symbol in matches[:args.limit]:
            print_symbol(symbol, directory, owners, sources[symbol.include], args.implementation)
        print(f"{len(matches)} declarations; showing {min(args.limit, len(matches))}")
    else:
        for symbol in matches[:args.limit]:
            deprecated = " [deprecated]" if symbol.deprecated else ""
            print(f"{symbol.include}:{symbol.line} [{symbol.kind}]{deprecated} | {owners.get(symbol.include, 'unmapped')}\n  {symbol.signature}")
        print(f"\n{len(matches)} matches; showing {min(args.limit, len(matches))}. Use show for the full adjacent source documentation.")
    return 0 if matches else 1


if __name__ == "__main__":
    try:
        sys.exit(run())
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
