# Provenance and primary sources

The source corpus consists of all 76 `.inc` files originally supplied in this project's root on 2026-10-14. The duplicate root files were subsequently removed to organize this repository around its skills. The reference snapshot under `includes/` preserves the supplied files byte for byte. The manifest records SHA-256 hashes so changed inputs can be distinguished from the original baseline. Original license and copyright notices remain in those reference files.

Version evidence comes from `amxmodx_version.inc` (`AMXX_VERSION_STR` 1.10.0.5487; changeset `8fc12670`) and `reapi_version.inc` (major 5, minor 29, numeric version 529359). No release date or guarantee that these are the newest upstream files is inferred. The target project's actual compiler includes and installed server modules decide availability.

Primary sources checked while creating the skills:

- [AMX Mod X API reference](https://www.amxmodx.org/api/) and [official builds](https://www.amxmodx.org/downloads-new.php).
- [AMXX source includes](https://github.com/alliedmodders/amxmodx/tree/master/plugins/include).
- [ReAPI source includes](https://github.com/rehlds/ReAPI/tree/master/reapi/extra/amxmodx/scripting/include), including hook enums and member get/set contracts.
- [ReHLDS](https://github.com/rehlds/ReHLDS) and [ReGameDLL_CS](https://github.com/rehlds/ReGameDLL_CS) for engine/game subsystem context.
- [Cvar creation](https://www.amxmodx.org/api/cvars/create_cvar), [binding](https://www.amxmodx.org/api/cvars/bind_pcvar_num), [event registration](https://www.amxmodx.org/api/amxmodx/register_event) and [threaded SQL ownership](https://www.amxmodx.org/api/sqlx/SQL_ThreadQuery).
- [Codex local skill discovery](https://learn.chatgpt.com/docs/build-skills) for the project-local `.agents/skills` layout.

Online master branches can differ from the supplied versions. The skills deliberately retrieve exact local declarations rather than filling missing APIs from a newer online page. When a local comment is incomplete or inconsistent, inspect the corresponding version's upstream implementation and compile a narrow example before relying on the disputed contract.

The supplied ESF include is an EvolutionXCore interface, not an invented `esf_*` namespace. The DoD/TFC/TS/NS APIs are retained in a separate skill because their presence in an include folder does not make them valid CS 1.6 dependencies.
