---
name: cs16-api-reference
description: Resolve exact AMX Mod X, CS 1.6, ReAPI and ReHLDS include contracts, locate native/forward/hook/member/constant definitions, and route API migrations against a project's actual compiler includes.
---

# CS 1.6 API reference and routing

Use this skill to discover an API, verify an uncertain declaration, choose a compatible modern implementation, or audit include coverage. For an implementation confined to a known domain, load its skill directly and use this reference only for the contracts it needs.

## Select the source set

Read [shared contracts](references/shared-contracts.md) once per plugin task. Identify the target game's directory, Pawn compiler include path, AMXX version and installed modules. The project's actual compile inputs take precedence. The bundled baseline is AMXX 1.10.0.5487 and ReAPI 5.29; never infer runtime availability from these files.

Reuse the project's existing environment record, normally `.agents/cs16-environment.md`, after checking the relevant paths. When the compiler/include selection is missing or changes, read [project toolchain memory](references/project-environment.md) for discovery, persistence and a reusable Markdown template. Save established settings in the consuming project and make the record discoverable through its project instructions.

The [coverage report](references/include-coverage.md) maps every supplied include to its primary domain skill. The [manifest](references/manifest.json) records fingerprints and dependency directives. Do not load the whole include corpus into context.

## Retrieve only the relevant contracts

Use [scripts/api_catalog.py](scripts/api_catalog.py), resolving its path relative to this skill directory:

```sh
python <this-skill>/scripts/api_catalog.py find TakeDamage --kind hook --include-dir <compiler-includes>
python <this-skill>/scripts/api_catalog.py show RG_CBasePlayer_TakeDamage --include-dir <compiler-includes>
python <this-skill>/scripts/api_catalog.py show m_flNextAttack --include-dir <compiler-includes>
python <this-skill>/scripts/api_catalog.py find reload --docs --include "reapi*" --include-dir <compiler-includes>
```

Replace angle-bracket paths with real quoted paths. Omit `--include-dir` only to investigate the explicitly labeled snapshot. `find` returns names, signatures and owners; `show` returns exact adjacent comments and declarations; `raw` searches all source text. Add `--implementation` when a stock's behavior matters. For the complete command contract, read [retrieval and maintenance](references/retrieval.md).

Scripts are optional implementation helpers, not a prerequisite for applying the guidance. If Python is unavailable, search/read the target includes directly with the available file tools and follow the same source-selection rules. Snapshot refresh is collection maintenance, not part of implementing each plugin.

Before calling a variadic native, read both its declaration and the selected member/selector's documented get/set parameters. Before registering a hook, read the hook enum entry's argument list and return type, not just the registration native. Check declaration tags, parameter numbering, invalid sentinels, ownership, allowed callback phase and version notes.

## Choose the domain

- Lifecycle, commands, deferred work, player sessions or custom natives: [plugin core](../cs16-amxx-plugin-core/SKILL.md).
- Cvars, config timing or gamedata: [cvars and config](../cs16-cvars-config/SKILL.md).
- Hook registration, argument edits or superceding a call: [ReAPI hooks](../cs16-reapi-hooks/SKILL.md).
- CS players, items, weapons, economy, rounds or rules on ReGameDLL: [ReAPI gameplay](../cs16-reapi-gameplay/SKILL.md).
- ReHLDS engine hooks, entity variables, usercmd or modern message interception: [engine](../cs16-rehlds-engine/SKILL.md).
- Reunion, Rechecker or voice extensions: [addons](../cs16-reapi-addons/SKILL.md).
- Uncovered entity/virtual/engine operations or stock-server compatibility: [Ham and Fakemeta](../cs16-entities-ham-fakemeta/SKILL.md).
- Stock CS/CZ or CSX statistics: [CStrike and stats](../cs16-cstrike-stats/SKILL.md).
- Presentation: [messages and UI](../cs16-messages-ui/SKILL.md).
- Plugin data: [containers](../cs16-data-containers/SKILL.md), [storage and SQL](../cs16-storage-sql/SKILL.md), [text parsing](../cs16-text-parsing/SKILL.md), [math and time](../cs16-math-time/SKILL.md), or [network and GeoIP](../cs16-network-geoip/SKILL.md).
- Includes for another GoldSrc game: [other mods](../goldsrc-other-mods/SKILL.md).

## Modernize with evidence

Read [modern API selection](references/modern-api-selection.md) when migrating old code. Prefer supported semantic hooks/natives over message inference, raw pdata offsets and emulated helpers for the same behavior. Preserve the project's declared server compatibility and interaction with other plugins. Do not describe a supported fallback as deprecated unless its source says so.

Compile against the selected include set when a compiler is available. State separately what compilation establishes and what still requires runtime checks. Cite local declarations by include name and line when explaining an API decision.
