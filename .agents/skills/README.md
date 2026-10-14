# CS 1.6 and GoldSrc API skills

This project-local collection contains 16 English-language skills covering all 76 supplied includes. Skills are grouped by implementation domain so an agent can load only the guidance relevant to the current plugin. Every include has one primary owner in the [coverage report](cs16-api-reference/references/include-coverage.md).

## Use in a project

Keep this entire collection under `<project>/.agents/skills/`. Codex discovers repository skills in that location and loads their instructions when a task matches their descriptions. You can also invoke a skill explicitly, for example:

```text
Use $cs16-reapi-gameplay to implement a spawn loadout using this project's compiler includes.
Use $cs16-cvars-config to replace deprecated cvar registration and bind the new values.
Use $cs16-api-reference to verify the exact callbacks and constants before migrating this plugin.
```

Copy the complete collection to another project's `.agents/skills` folder. Keep the skill directories as siblings: the domain skills share `cs16-api-reference` for source retrieval and common contracts. No user configuration changes or global installation are required. If newly created skills do not appear, restart Codex. See the [official local skill discovery documentation](https://learn.chatgpt.com/docs/build-skills).

An agent outside Codex can read the appropriate `SKILL.md` files directly. Automatic discovery in another agent depends on that agent's own skill loader.

For repeat use, save the consuming project's established compiler/include selections in its existing toolchain notes or `.agents/cs16-environment.md`. The shared contracts direct the assistant to read and validate that context before rediscovering paths. Use [the template](cs16-api-reference/assets/cs16-environment.template.md) and [project toolchain memory guide](cs16-api-reference/references/project-environment.md), including its short `AGENTS.md` pointer. Actual host paths belong to the consuming project rather than these portable skills.

## Choose a skill

| Skill | Work it supports |
| --- | --- |
| [cs16-api-reference](cs16-api-reference/SKILL.md) | Exact API lookup, source selection, coverage and migration routing |
| [cs16-amxx-plugin-core](cs16-amxx-plugin-core/SKILL.md) | Plugin lifecycle, clients, commands, tasks and inter-plugin APIs |
| [cs16-cvars-config](cs16-cvars-config/SKILL.md) | Cvar creation, binding, changes, configs and gamedata |
| [cs16-reapi-hooks](cs16-reapi-hooks/SKILL.md) | ReAPI hookchains, callback signatures and return semantics |
| [cs16-reapi-gameplay](cs16-reapi-gameplay/SKILL.md) | ReGameDLL players, weapons, rounds, rules and typed members |
| [cs16-rehlds-engine](cs16-rehlds-engine/SKILL.md) | ReHLDS engine hooks, entity variables, movement and messages |
| [cs16-reapi-addons](cs16-reapi-addons/SKILL.md) | Reunion, Rechecker and VoiceTranscoder integration |
| [cs16-entities-ham-fakemeta](cs16-entities-ham-fakemeta/SKILL.md) | Entity work, Ham, Fakemeta, engine and compatibility fallbacks |
| [cs16-cstrike-stats](cs16-cstrike-stats/SKILL.md) | Stock CS/CZ gameplay APIs, CSX events and statistics |
| [cs16-messages-ui](cs16-messages-ui/SKILL.md) | User messages, temporary entities, menus, HUD and translations |
| [cs16-data-containers](cs16-data-containers/SKILL.md) | Arrays, tries, stacks, datapacks and sorting |
| [cs16-storage-sql](cs16-storage-sql/SKILL.md) | Files, nVault, SQLX and legacy persistence migration |
| [cs16-text-parsing](cs16-text-parsing/SKILL.md) | Strings, regex, JSON, INI and SMC parsing |
| [cs16-math-time](cs16-math-time/SKILL.md) | Float math, vectors, geometry and time domains |
| [cs16-network-geoip](cs16-network-geoip/SKILL.md) | Nonblocking sockets and GeoIP |
| [goldsrc-other-mods](goldsrc-other-mods/SKILL.md) | DoD, TFC, TS, NS and ESF; prevents their APIs leaking into CS plugins |

## Query the actual compiler includes

Python 3.10 or newer is sufficient; retrieval and validation use only the standard library. Run commands from the project root, or use the script's absolute path.

```sh
python .agents/skills/cs16-api-reference/scripts/api_catalog.py find TakeDamage --kind hook --include-dir "path/to/compiler/includes"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py show RG_CBasePlayer_TakeDamage --include-dir "path/to/compiler/includes"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py show create_cvar --include-dir "addons/amxmodx/scripting/include"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py show m_pActiveItem --include "reapi_gamedll_const.inc" --include-dir "path/to/compiler/includes"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py raw WeaponList --include "*message*" --include-dir "path/to/compiler/includes"
```

Always pass `--include-dir` when the target compiler's include directory is known. That source set is read directly on every invocation and is never merged with the bundled snapshot. Without it, the tool clearly identifies the supplied reference snapshot: AMX Mod X 1.10.0.5487 and ReAPI 5.29 (`REAPI_VERSION=529359`). This baseline is not a promise about the target server's installed modules.

The standalone repository keeps its reference snapshot inside `cs16-api-reference/references/includes/`; use your own SDK for plugin compilation. The original duplicate `.inc` files have been removed from the repository root.

The index preserves signatures, tags, defaults, adjacent documentation, enum memberships, file paths and line numbers. It retains alternate preprocessor branches and unevaluated expressions. Use `raw` or read the include for constructs outside its lexical parser; use the Pawn compiler to resolve active definitions. `--docs` searches adjacent documentation as well as names; `--json` returns structured results.

## Maintain the collection

The scripts are optional helpers. Keep them alongside the API-reference skill for precise local lookups, reproducible example compilation and collection maintenance. Python 3.10+ is required only when running them; an assistant can otherwise read/search local includes with its usual file tools. Routine plugin work uses `api_catalog.py` with `--include-dir`; snapshot refresh is a maintainer operation.

The [manifest](cs16-api-reference/references/manifest.json) records an owner, SHA-256 hash, dependency directives and declaration counts for every include. Refresh explicitly after reviewing source changes:

```sh
python .agents/skills/cs16-api-reference/scripts/api_catalog.py coverage --include-dir "path/to/updated/includes"
python .agents/skills/cs16-api-reference/scripts/refresh_snapshot.py --include-dir "path/to/complete/includes"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py validate
python -B -m unittest discover -s .agents/skills/cs16-api-reference/scripts/tests -v
```

`coverage` reports missing, newly added and changed includes. `refresh_snapshot` only changes this collection's bundled reference files, fingerprints and coverage report. It preserves source bytes and refuses new or missing filenames until the ownership map is updated. It does not rewrite the domain guidance: inspect changed contracts and adjust the affected skill before treating an update as complete.

Use [the example compiler helper](cs16-api-reference/scripts/validate_examples.py) with an existing AMXX compiler to check the supplied `.sma` examples. It writes generated binaries only to a temporary directory. Compilation checks syntax and API availability; live-server behavior still requires the target modules, gamedata and gameplay checks.

See the [validation report](cs16-api-reference/references/validation.md) for the checks performed on the supplied baseline.

The supplied includes retain their original copyright and license notices. The snapshot is a portable source reference, not a replacement installation of server modules or a complete server SDK. [Provenance and primary sources](cs16-api-reference/references/provenance.md) describe the baseline.
