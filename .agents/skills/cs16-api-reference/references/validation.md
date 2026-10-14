# Validation report

Validated on 2026-10-14 against the supplied project includes.

The initial compilation and root-versus-snapshot checks below were performed before the duplicate `.inc` files were removed from the repository root. The maintained source baseline is now the snapshot inside the API-reference skill. New plugin work should use an explicit external compiler include directory.

## Source baseline

- 76 includes, 44,431 source lines, AMX Mod X 1.10.0.5487 (`8fc12670`) and ReAPI 5.29 (`REAPI_VERSION=529359`).
- 16 English-language skills with automatic-selection metadata and an explicit primary owner for every include.
- 7,575 lexical symbol declarations: 1,455 natives, 80 forwards, 380 stocks, 13 stock variables, 185 named enums, 3,920 constants, 62 function-like macros, 793 hook IDs and 687 member selectors. Alternate preprocessor branches remain separate declarations.
- Before removal of the root duplicates, SHA-256 and byte comparisons confirmed that all 76 original includes matched the preserved reference snapshot.

## Collection and retrieval checks

| Check | Result |
| --- | --- |
| Bundled skill-creator `quick_validate.py` | All 16 skills passed |
| UI YAML parsing, description lengths, prompt references and invocation policy | All 16 metadata files passed |
| Coverage, ownership, snapshot hashes and local Markdown links | Passed |
| Standard-library unittest suite | 11 tests passed |
| Every supplied native/forward/stock declaration header discoverable | Passed for all 76 includes |
| Explicit compiler includes replace the bundled source set | Passed; missing APIs are not filled from the snapshot |
| Comments, escaped Pawn strings, enum expressions and operator overloads | Passed |
| Raw fallback for an unsupported/broken declaration | Passed |
| Complete collection relocated to a separate temporary directory | Validation and source lookup passed using the relocated sources |

## Pawn examples

Used the official [AMXX 1.10.0.5487 Windows release](https://github.com/alliedmodders/amxmodx/releases/tag/1.10.0.5487) compiler with the original project root as the explicit include directory.

| Example | Result |
| --- | --- |
| [Session-aware modern task](../../cs16-amxx-plugin-core/assets/session-task.sma) | Compiled without errors or warnings |
| [Bounded cvar and config timing](../../cs16-cvars-config/assets/modern-cvar.sma) | Compiled without errors or warnings |
| [ReAPI pre-damage argument edit](../../cs16-reapi-hooks/assets/damage-scale.sma) | Compiled without errors or warnings |
| [ReGameDLL post-spawn loadout](../../cs16-reapi-gameplay/assets/spawn-loadout.sma) | Compiled without errors or warnings |
| [Modern ReHLDS message observer](../../cs16-rehlds-engine/assets/message-observer.sma) | Compiled without errors or warnings |
| [JSON type checking and child-handle ownership](../../cs16-text-parsing/assets/json-handles.sma) | Compiled without errors or warnings |

Generated `.amxx` files were confined to temporary storage. This verification establishes example syntax and API availability in the supplied compile inputs. Runtime behavior depends on the target server/modules; no live gameplay execution is claimed.

## Reproduce

```sh
python .agents/skills/cs16-api-reference/scripts/api_catalog.py validate
python .agents/skills/cs16-api-reference/scripts/api_catalog.py coverage --include-dir "path/to/compiler/includes"
python -B -m unittest discover -s .agents/skills/cs16-api-reference/scripts/tests -v
python .agents/skills/cs16-api-reference/scripts/validate_examples.py --compiler "path/to/amxxpc" --include-dir "path/to/compiler/includes"
```

Use the target project's compiler inputs for new work. After refreshing sources, review changed contracts and rerun the relevant checks; this report describes the supplied baseline rather than all possible later versions.
