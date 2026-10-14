# CS 1.6 AMXX & ReAPI Development Skills

A repository of reusable, English-language skills for AI-assisted Counter-Strike 1.6 plugin development in Pawn with **AMX Mod X and ReAPI**, including ReGameDLL_CS and ReHLDS integrations.

The skills guide API selection, implementation and review: prefer supported modern natives and semantic forwards/hooks, preserve game behavior, use the correct constants and tags, and verify contracts against the project's actual compiler includes.

## Use with your existing development environment

Use your own AMXX compiler, local includes, project build command and server modules. The skills supply guidance, references and optional development helpers.

1. Copy the contents of this repository's `.agents/skills/` into your project's `.agents/skills/`, preserving the sibling skill folders and their resources. Merge with any skills already present in the destination.
2. Give the assistant the include directory used by your Pawn compiler, along with the intended AMXX/ReAPI versions and server capabilities when known.
3. Let the assistant select the relevant skill, or invoke it explicitly:

```text
Use $cs16-reapi-gameplay to implement this spawn loadout.
Use my existing compiler includes at "C:/server/addons/amxmodx/scripting/include"
and preserve this project's declared server compatibility.
```

For API discovery or a migration spanning multiple domains:

```text
Use $cs16-api-reference to verify the exact natives, hooks and constants
available in my local includes before updating this plugin.
```

The `.agents/skills` layout supports project-local Codex skill discovery. Other assistants can read the relevant `SKILL.md` directly or use their own skill loader. See the [portable usage guide](.agents/skills/README.md) for discovery and integration details.

### Remember the project's compiler and includes

The shared skill instructions direct the assistant to reuse established toolchain notes before discovering paths again. During plugin implementation or environment setup, it can record the selected compiler executable, include directories, working directory and build command in the consuming project's `.agents/cs16-environment.md`, with selection evidence and verification status.

Use [the environment template](.agents/skills/cs16-api-reference/assets/cs16-environment.template.md) when that project has no existing toolchain record. Keep actual machine-specific paths in the consuming project. The assistant checks relevant paths on reuse and updates stale selections from current user directions and build configuration.

For persistent discovery, add a short instruction to the consuming project's `AGENTS.md` to read that profile. The [project toolchain memory guide](.agents/skills/cs16-api-reference/references/project-environment.md) includes the exact pointer and explains how to preserve existing instructions, ordered include paths and partially known environments. Existing maintained toolchain notes can be reused in place of the default filename.

## Available skills

The collection contains **16 skills**, organized by implementation domain and grounded in **76 analyzed include files**. Read only the domain references needed for the current task.

| Skill | Purpose |
| --- | --- |
| [cs16-api-reference](.agents/skills/cs16-api-reference/SKILL.md) | Exact API lookup, source selection, coverage and migration routing |
| [cs16-amxx-plugin-core](.agents/skills/cs16-amxx-plugin-core/SKILL.md) | Plugin lifecycle, client sessions, commands, tasks and inter-plugin APIs |
| [cs16-cvars-config](.agents/skills/cs16-cvars-config/SKILL.md) | Modern cvars, bindings, config execution and gamedata |
| [cs16-reapi-hooks](.agents/skills/cs16-reapi-hooks/SKILL.md) | Hookchain signatures, pre/post phases and dispatch/return semantics |
| [cs16-reapi-gameplay](.agents/skills/cs16-reapi-gameplay/SKILL.md) | ReGameDLL players, inventory, weapons, teams, rounds and game rules |
| [cs16-rehlds-engine](.agents/skills/cs16-rehlds-engine/SKILL.md) | Engine hooks, typed state, movement and modern message interception |
| [cs16-reapi-addons](.agents/skills/cs16-reapi-addons/SKILL.md) | Reunion, Rechecker and VoiceTranscoder integration |
| [cs16-entities-ham-fakemeta](.agents/skills/cs16-entities-ham-fakemeta/SKILL.md) | Entities, HamSandwich, Fakemeta and supported compatibility paths |
| [cs16-cstrike-stats](.agents/skills/cs16-cstrike-stats/SKILL.md) | CStrike APIs, CSX forwards and statistics layouts |
| [cs16-messages-ui](.agents/skills/cs16-messages-ui/SKILL.md) | Messages, temporary entities, HUD, menus and localization |
| [cs16-data-containers](.agents/skills/cs16-data-containers/SKILL.md) | Arrays, tries, iterators, stacks, datapacks and sorting |
| [cs16-storage-sql](.agents/skills/cs16-storage-sql/SKILL.md) | Files, nVault, SQLX and asynchronous persistence |
| [cs16-text-parsing](.agents/skills/cs16-text-parsing/SKILL.md) | Strings, regex, JSON, INI and SMC |
| [cs16-math-time](.agents/skills/cs16-math-time/SKILL.md) | Float arithmetic, vectors, geometry and time domains |
| [cs16-network-geoip](.agents/skills/cs16-network-geoip/SKILL.md) | Nonblocking sockets and modern GeoIP lookup |
| [goldsrc-other-mods](.agents/skills/goldsrc-other-mods/SKILL.md) | DoD/TFC/TS/NS/ESF boundaries and identification of APIs belonging to other games |

Use ReAPI where the deployment supports the requested semantic operation. Keep supported Ham, Fakemeta, engine or CStrike paths when the feature or compatibility contract needs them. Verify availability and behavior before replacing an API solely because a newer name exists.

## Source policy

**The includes used by the target project's compiler are the authority for implementation.** Pass their directory explicitly to the lookup helper. It reads those files on every invocation and never fills missing APIs from a different source set.

The repository root contains documentation and the skill collection. A single versioned reference snapshot remains at `.agents/skills/cs16-api-reference/references/includes/`, with hashes and include ownership recorded in the [manifest](.agents/skills/cs16-api-reference/references/manifest.json). Its baseline is AMXX **1.10.0.5487** and ReAPI **5.29** (`REAPI_VERSION=529359`). It supports reference lookup and collection maintenance when an external SDK is unavailable.

Omitting `--include-dir` selects that labeled snapshot. For work on a real plugin, provide the project's include path. Snapshot declarations do not establish which modules are installed on the target server or which conditional definitions the compiler activates.

## Optional scripts

The [scripts directory](.agents/skills/cs16-api-reference/scripts/) belongs to the shared API-reference skill because its helpers are reused by the domain skills. They require **Python 3.10+** and use the standard library. An assistant can also search and read the local includes with ordinary file tools when Python is unavailable.

| Helper | Audience and purpose |
| --- | --- |
| [api_catalog.py](.agents/skills/cs16-api-reference/scripts/api_catalog.py) | Plugin developers: retrieve signatures, adjacent comments, hook parameters, members and constants from local includes; maintainers: validate coverage and resources |
| [validate_examples.py](.agents/skills/cs16-api-reference/scripts/validate_examples.py) | Developers/maintainers: compile the supplied examples with an explicitly selected existing AMXX compiler and include directory |
| [refresh_snapshot.py](.agents/skills/cs16-api-reference/scripts/refresh_snapshot.py) | Maintainers: update the bundled reference snapshot and manifest after reviewing a complete source set |

### Query local APIs

Run from the target project root, replacing the quoted include path with your compiler's actual directory:

```sh
python .agents/skills/cs16-api-reference/scripts/api_catalog.py find TakeDamage --kind hook --include-dir "path/to/compiler/includes"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py show RG_CBasePlayer_TakeDamage --include-dir "path/to/compiler/includes"
python .agents/skills/cs16-api-reference/scripts/api_catalog.py show create_cvar --include-dir "path/to/compiler/includes"
```

Use `--docs` to search descriptions, `--implementation` to inspect complete stock/enum bodies, or `--json` for structured output. `raw` provides literal source lookup for constructs outside the lexical parser. The Pawn compiler resolves active preprocessor branches, types and expressions.

### Validate the collection and examples

```sh
python .agents/skills/cs16-api-reference/scripts/api_catalog.py validate
python -B -m unittest discover -s .agents/skills/cs16-api-reference/scripts/tests -v
python .agents/skills/cs16-api-reference/scripts/validate_examples.py --compiler "path/to/amxxpc" --include-dir "path/to/compiler/includes"
```

The example helper writes generated binaries to temporary storage. Compile success verifies syntax and available declarations; game behavior is verified on the intended server stack. See the [validation report](.agents/skills/cs16-api-reference/references/validation.md) for the baseline checks.

### Maintain the reference snapshot

Snapshot refresh is a maintenance operation, separate from querying a user's SDK. It requires the complete mapped corpus; missing or new filenames require a deliberate coverage/ownership update. It preserves the input files and updates only the collection's reference resources. Review affected skill guidance after source changes.

See [retrieval and maintenance](.agents/skills/cs16-api-reference/references/retrieval.md) for command details and [include coverage](.agents/skills/cs16-api-reference/references/include-coverage.md) for the source-to-skill map.

## Provenance

The bundled include files retain their original copyright and license notices. The [provenance reference](.agents/skills/cs16-api-reference/references/provenance.md) records the analyzed baseline and primary upstream sources. Use the applicable upstream notices when redistributing those files.
