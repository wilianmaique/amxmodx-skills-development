# Retrieval and maintenance

The helper is a read-only lexical parser with no network dependency or generated symbol cache. It parses the chosen `.inc` files on each request. Python 3.10+ is required.

## Commands

| Command | Purpose |
| --- | --- |
| `list` | List includes, line counts, declaration counts and primary owners |
| `find <text>` | Case-insensitive symbol-name substring search; exact names and prefixes sort first |
| `show <symbol>` | Exact case-insensitive name lookup, with adjacent source documentation and line numbers |
| `raw <text>` | Literal case-insensitive search over all source text, including preprocessor directives and comments |
| `coverage` | Compare the selected include set to the manifest; report missing, unmapped and changed files |
| `validate` | Validate the collection's skill coverage, fingerprints, metadata and local Markdown resource links |

Useful options: `--include-dir <directory>`, repeated `--include <filename-or-glob>`, `--kind <kind>`, `--limit <positive-number>`, `--json`, `--docs` for description search and `--implementation` for complete stock or enum bodies. `raw` also accepts `--context <lines>`.

Kinds are `native`, `forward`, `stock`, `stock-variable`, `enum`, `constant`, `hook`, `member` and `macro`. Kinds are routing hints, not Pawn types. Numeric enum values, `#if` branches, overloaded dispatch and aliases are not evaluated. Declarations in alternate branches remain separate records. The original files and compiler decide their actual availability.

The explicit directory must contain the target compiler's includes. It completely replaces the snapshot for that invocation, including when an API is missing. There is no implicit search of unrelated projects, system folders or network sources. Queries do not write files.

The assistant can reuse paths saved in the consuming project's environment notes following [project toolchain memory](project-environment.md). The current helpers still take explicit `--include-dir`/`--compiler` arguments; they do not automatically read or execute a Markdown profile.

Exit codes: `0` for matches or successful validation; `1` for no matches, missing/unmapped coverage or validation failures; `2` for invalid arguments, unreadable files or parse errors. `coverage` reports changed fingerprints without treating a deliberate version change alone as a failure. `validate` always checks this pack's snapshot, regardless of query source options.

## Inspect contracts

1. Search a feature keyword or symbol fragment with `find`, limiting by filename/kind where possible.
2. Use `show` for the selected native and hook/member/selector entries. A registration native's generic variadic signature is not enough to define a callback or member access.
3. Follow the owning skill for behavioral guidance. Read raw source surrounding any conditional macro, alias or incomplete comment.
4. Compile the resulting Pawn against the explicit target include path. Do not treat lexical discovery as proof of an active preprocessor branch.

## Refresh reviewed sources

Run `refresh_snapshot.py --include-dir <complete-source-directory>` after reviewing new includes. It refuses missing or unmapped filenames, reads and parses the full source set before replacement, preserves each source file's bytes and updates hashes, version macros, dependency directives, declaration counts and `include-coverage.md`. It never edits the input source directory or deletes files.

For a new include, add its primary owner to `manifest.json`, document it in that skill and update routing before refreshing. Recheck exact callback signatures, ownership and modern-selection guidance after API changes. The original `snapshot_date` identifies the supplied baseline; the fingerprints identify the current bundled contents.

Run `api_catalog.py validate`, the bundled unittest suite and the skill-creator frontmatter validator if available. Use `validate_examples.py --compiler <amxxpc> --include-dir <compiler-includes>` to compile all examples into temporary storage. The helper does not download a compiler or alter the user's build configuration.
