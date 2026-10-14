# Structured parsing contracts

## Regex state

`regex_compile` uses text flags; `_ex` uses the named bit flags declared by this include. A direct rename can change the expected arguments. `regex_match`, `regex_match_c`, match-all helpers and `regex_match_simple` also differ in compiled-handle ownership and return semantics.

Read capture/subpattern indexing and the selected match count before calling `regex_substr`. Reusing a compiled handle can replace its stored match state. Copy a capture that must survive another match. Free owned handles via `regex_free`; distinguish a negative failure sentinel from a valid handle and from no match.

Read `REGEX_FORMAT_*` and replacement flags before `regex_replace`, particularly when capture substitution or literal replacement text matters. Bound pattern/input work to the feature's actual needs; compile a known repeated pattern once instead of recompiling it in a per-frame hook.

## JSON ownership and types

The supplied `json_array_get_value`, `json_object_get_value`, `json_object_get_value_at` and `json_get_parent` document returned handles that must be freed. They are not borrowed numeric references merely because the underlying value belongs to a container. Free valid returned handles on every path as well as the owned root; do not invent one universal ownership-transfer rule for all setters/getters.

Check `json_get_type` and `json_object_has_value` using the expected `JSONType` before reading a typed value. A false boolean, zero number and empty string are valid present data. Dot notation is optional and can make literal dotted keys inaccessible, so choose it deliberately.

`json_deep_copy` provides an independent copy when that is the intended contract. The short setter comments do not fully describe every implementation ownership detail; for a retained value replaced/removed in a parent, inspect the same-version implementation before relying on its lifetime.

`json_serial_size`, `json_serial_to_string` and `json_serial_to_file` have separate size/termination/pretty-print contracts. Allocate based on the selected size mode and check serialization/write outcomes. A syntactically valid JSON root can still contain an invalid application configuration.

## INI callbacks

`INI_SetReaders` takes the key/value callback first and optional section callback second. The callbacks return bool to continue/stop parsing and receive invalid-token/equal/quote or bracket/extra-token flags plus the current token and user data. Copy the exact source prototypes; they are not the same as the SMC callbacks.

Use these flags when the requested configuration rejects malformed entries. `INI_ParseFile` reports line/column and accepts a data value. `INI_SetRawLine`, parse-start and parse-end callbacks have their own signatures; retrieve them before implementation.

## SMC callbacks

SMC readers return `SMCResult`, including the documented continue/halt behavior. New-section, key/value and end-section callbacks define a hierarchy; track section depth/state and reject impossible transitions when the application needs a fixed schema. Quoting is stripped by the parser as documented.

Distinguish parser errors from a callback-requested halt. Destroy the `SMCParser:` handle after the intended parse lifetime and use its error-description API for useful diagnostics. A config reload should publish fully validated new settings rather than retain an accidental mixture after a failed parse.
