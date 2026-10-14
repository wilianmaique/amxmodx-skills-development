---
name: cs16-text-parsing
description: Parse and transform AMXX strings, UTF-8 text, regex, JSON, INI and SMC configuration for CS 1.6 plugins with modern supported helpers, exact parser callbacks and complete handle ownership.
---

# Strings and structured parsing

Primary includes: `string.inc`, `string_const.inc`, `string_stocks.inc`, `regex.inc`, `json.inc`, `textparse_ini.inc`, `textparse_smc.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Retrieve exact signatures, error constants and callback prototypes through [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py), using the target compiler includes.

## String operations

- Most writable string natives exclude the terminator from maximum length; use `charsmax` where documented. Check actual byte/character counts for multibyte text and raw data.
- Prefer `argparse`/`argbreak` to deprecated `strbreak`, and `replace_string` to the older `replace_all` stock when its semantics fit. Preserve quoting, case sensitivity and cursor progress.
- Use `formatex` with independent inputs; use `format` when the destination is also a formatting input. Match `%f`, `%d`, `%s`, translation targets and vararg types. Player/config text is data, not a format string.
- Use maintained multibyte/category helpers and `string_const.inc` when UTF-8/category behavior matters; ASCII character helpers do not become Unicode-aware by renaming them.
- Parse numeric text deliberately. A numeric conversion that returns zero does not prove the input was valid. Check empty input, allowed syntax and range before applying gameplay settings.

## Regex

Compile a reused pattern once and free its `Regex:` handle at the matching lifetime. Prefer `regex_compile_ex` with named flags where supported; select single-match versus match-all based on the requested result. `regex_substr` depends on the match state/capture layout of the selected API, so inspect it before retrieving groups.

Respect declared compile/match error sentinels and output error codes. A valid compiled pattern with no match differs from an invalid pattern. Read [structured parsing contracts](references/structured-parsing.md) for handles and replacement flags.

## JSON

Validate `JSON:` handles against `Invalid_JSON`, check value type/key presence, and use typed getters. Dot notation changes lookup semantics for keys containing dots. Do not infer a key is absent solely from a false/zero returned value.

Free every owned handle, including child/parent handles returned by getters when the include says they require `json_free`. Use `json_deep_copy` when independent copied data is required. Setter/replacement operations can remove existing values; check the documented behavior before reusing a retained child.

The [JSON handle example](assets/json-handles.sma) demonstrates type checks and cleanup for a separately returned child handle. `json_validate`'s schema semantics come from this module's contract; do not describe it as an arbitrary external JSON Schema specification.

## INI and SMC

Use an INI parser for flat sections/key-value syntax, and SMC for the documented hierarchical syntax. Create/destroy the matching tagged parser. Retrieve `INI_SetReaders`/`SMC_SetReaders` before implementing callbacks: their signatures, flags and return families differ.

Check parse errors and line/column information, preserve nested section state for SMC, and use callback `data` to associate parser state where needed. Rebuild settings only after a complete valid parse; avoid leaving half-updated live configuration after a syntax failure when the feature requires consistency.

Compile and verify malformed input, missing/wrong-type values, truncation, quoted strings and cleanup relevant to the parser. Do not assume examples from a newer include describe the target version.
