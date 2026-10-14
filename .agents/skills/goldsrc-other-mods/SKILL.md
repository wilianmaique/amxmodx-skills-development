---
name: goldsrc-other-mods
description: Resolve AMXX APIs for Day of Defeat, Team Fortress Classic, The Specialists, Natural Selection and ESF/EvolutionXCore, and prevent those game-specific natives/constants/forwards from being used as CS 1.6 APIs.
---

# Other GoldSrc mods

Primary includes: `dodconst.inc`, `dodfun.inc`, `dodstats.inc`, `dodx.inc`, `esf.inc`, `esf_const.inc`, `ns.inc`, `ns_const.inc`, `tfcconst.inc`, `tfcstats.inc`, `tfcx.inc`, `tsconst.inc`, `tsfun.inc`, `tsstats.inc`, `tsx.inc`.

Use this skill when the requested target is one of these games, when identifying a misleading include/symbol collision, or when porting code between mods. Their presence in the folder does not make them valid CS 1.6 dependencies. ReGameDLL_CS hooks and CS weapon/team enums are not a modernization path for unrelated game DLLs.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md) for source/type/lifetime rules. Query [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py) with a specific `--include` filter because stats/forwards have repeated names across mods.

## Route by actual game

| Game/interface | Includes | Contracts to inspect |
| --- | --- | --- |
| Day of Defeat | `dodx`, `dodfun`, `dodstats`, `dodconst` | Classes/teams/prone/scope/stamina, weapon/ammo and score/objective/explosion forwards |
| Team Fortress Classic | `tfcx`, `tfcstats`, `tfcconst` | Class/weapon/ammo/goalitem/feign/alliance data and stats event callbacks |
| The Specialists | `tsx`, `tsfun`, `tsstats`, `tsconst` | Weapons/ammo, powers/stunts/slow-motion, module version and stats callbacks |
| Natural Selection | `ns`, `ns_const` | Gameplay mode, classes/masks/resources/energy/upgrades/structures, round/team/spawn and particles |
| ESF / supplied EvolutionXCore | `esf`, `esf_const` | Declared `getClient*`/`setClient*` power/ki/health/movement/action APIs and `EvolutionXCore` module dependency |

Read [mod boundaries](references/mod-boundaries.md) for identity and legacy caveats. Retrieve every needed constant and callback from that game's include; do not infer it from a CS analog.

## Modernize within the target

Prefer the game's declared module forward/native for the actual event. Use a supported Ham method where the target mod and installed hamdata provide it. The supplied `ns_takedamage` is explicitly deprecated in favor of Ham; verify the correct method/execute parameters and intentional hook propagation.

Some older stats includes expose `register_statsfwd`; the TS include labels this interface deprecated. Do not blindly call it in a new plugin or assume the equivalent CSX registration behavior. Inspect the module's current callback requirements before changing an existing compatibility path.

`esf.inc` is an EvolutionXCore API with mixed-case `getClientKI`/`setClientKI` and related names. It does not declare a generic `esf_get_ki` native. Do not invent modern replacements for sparse legacy declarations. State a missing contract and consult same-version module source if it matters.

## Preserve mod-specific state

Classes, teams, weapon IDs, stats layouts, ammo banks, masks and particle handles belong to the selected game/module. `client_damage`, `client_death`, `custom_weapon_*`, `xmod_*` and stats query names can collide with CSX names while having different surrounding contracts.

For an actual CS plugin, remove an accidental dependency only after finding the supported CS/ReAPI equivalent for the requested feature; do not import one of these modules just to resolve a similarly named symbol. For a cross-mod plugin, separate compile/runtime capabilities deliberately rather than including every mod header in the same file.

Compile against the chosen mod's includes/modules. Verify mode/class/round and supported bot/version behavior where applicable; do not label a CS-only compile as proof that the other mod works.
