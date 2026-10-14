#!/usr/bin/env python3
"""Compile the collection's Pawn examples with an explicitly chosen AMXX compiler.

Generated binaries are isolated in a validated temporary directory and removed
after checking. This does not download tools or change any server/build config.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
import api_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", required=True, help="Path to amxxpc.exe or amxxpc")
    parser.add_argument("--include-dir", help="Exact compiler include directory; defaults to the labeled bundled snapshot")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    compiler = Path(args.compiler).expanduser().resolve()
    if not compiler.is_file():
        raise ValueError(f"Compiler not found: {compiler}")
    include_dir, label = api_catalog.source_directory(args.include_dir)
    examples = sorted(api_catalog.PACK_DIR.glob("*/assets/*.sma"))
    if not examples:
        raise ValueError("The collection has no Pawn examples")
    results = []
    temp_root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix="cs16-example-check-", dir=temp_root) as directory:
        output_dir = Path(directory).resolve()
        if output_dir.parent != temp_root:
            raise ValueError(f"Unexpected temporary output path: {output_dir}")
        for example in examples:
            binary = output_dir / f"{example.parent.parent.name}-{example.stem}.amxx"
            if binary.resolve().parent != output_dir:
                raise ValueError(f"Invalid example output path: {binary}")
            completed = subprocess.run(
                [str(compiler), str(example), f"-i{include_dir}", f"-o{binary}"],
                cwd=compiler.parent, capture_output=True, text=True, errors="replace", timeout=30,
            )
            diagnostics = completed.stdout + completed.stderr
            has_warnings = bool(re.search(r"\bwarning\s+\d+\s*:", diagnostics, re.I))
            has_errors = bool(re.search(r"\b(?:fatal\s+)?error\s+\d+\s*:", diagnostics, re.I))
            ok = completed.returncode == 0 and binary.is_file() and binary.stat().st_size > 0 and not has_warnings and not has_errors
            results.append({"example": str(example.relative_to(api_catalog.PACK_DIR)),
                            "ok": ok, "returncode": completed.returncode,
                            "warnings": has_warnings, "errors": has_errors,
                            "diagnostics": diagnostics if not ok else diagnostics.splitlines()[0] if diagnostics else ""})
    summary = {"ok": all(result["ok"] for result in results), "compiler": str(compiler),
               "include_dir": str(include_dir), "source_policy": label, "examples": results}
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Includes: {include_dir}\nPolicy: {label}")
        for result in results:
            print(f"{'PASS' if result['ok'] else 'FAIL'}: {result['example']}")
            if not result["ok"]:
                print(result["diagnostics"])
        print(f"{sum(result['ok'] for result in results)}/{len(results)} examples compile without warnings. Binaries were kept only in temporary storage.")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
