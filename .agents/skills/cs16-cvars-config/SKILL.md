---
name: cs16-cvars-config
description: Create, bind and react to AMXX cvars; initialize config-dependent CS 1.6 plugin state at the correct phase; use gameconfig gamedata without guessed offsets or addresses.
---

# Cvars, configs and gamedata

Primary includes: `cvars.inc`, `gameconfig.inc`. Lifecycle/config execution support comes from `amxmodx.inc`.

Read the [shared contracts](../cs16-api-reference/references/shared-contracts.md). Query native signatures and `FCVAR_*`/`CvarBounds` definitions in the target includes with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py).

## Modern cvars

- Prefer `create_cvar` to deprecated `register_cvar` for new registrations. Supply a useful description, named flags and meaningful bounds. Bounds are floating-point parameters even for integer settings; do not invert min/max.
- A pre-existing cvar keeps its existing value; registration defaults apply only when first created. Do not set defaults again in startup code and erase an administrator's configured value.
- Cache handles from `create_cvar` or `get_cvar_pointer`. Check a pointer obtained for an optional external cvar before use. Prefer `get_pcvar_*`/`set_pcvar_*` over repeated name lookups; prefer bound values in frequently executed callbacks.
- Use `bind_pcvar_num`, `bind_pcvar_float` or `bind_pcvar_string` for global/static storage of the appropriate type. A local variable is invalid and a variable cannot bind to more than one cvar. Read `bind_pcvar_string` for its length contract.
- Use `hook_cvar_change` for derived-state updates or side effects. Its callback is `(pcvar, const old_value[], const new_value[])`. Bindings update stored values; they do not rebuild dependent menus, caches, schedules or weapon state automatically.
- Avoid recursion when a change callback normalizes the same cvar. Compare before writing or temporarily disable its hook using the stored `cvarhook:` handle.
- Use `OnConfigsExecuted` when derived values depend on all startup config files. Generate a config through `AutoExecConfig` if the project uses generated configs; follow existing naming and destination conventions.

The [modern cvar example](assets/modern-cvar.sma) demonstrates bounded registration, Float binding and config-dependent initialization. Inspect [configuration pitfalls](references/configuration.md) for bounds, client queries and gamedata.

## Existing server cvars

Use `get_cvar_pointer` for engine/game cvars rather than registering a second plugin setting under their names. A cvar's existence does not establish the semantics of a particular ReGameDLL build. When a requested behavior can be configured by an existing server cvar, verify its target-version contract before writing an emulation hook. These include files do not enumerate every runtime engine/game cvar.

Do not invent undocumented cvar names or describe a plugin cvar as a built-in server setting. Keep server changes within the requested feature and preserve administrator values.

## Gamedata

Use `LoadGameConfigFile`, `GameConfGetOffset`, `GameConfGetClassOffset`, `GameConfGetKeyValue` and `GameConfGetAddress` according to the selected platform and game. Read their individual failure sentinels. Keep the `GameConfig:` handle until dependent retrieval is complete and close it with `CloseGameConfigFile`.

Prefer typed ReAPI members or semantic natives for exposed CS fields. A gamedata address is a raw address, not an entity index or handle. Do not dereference it merely because a lookup returned a nonzero value.

Compile changes and verify defaults, startup config overrides, boundary values and live cvar changes. Include client-session validation for asynchronous `query_client_cvar` callbacks.
