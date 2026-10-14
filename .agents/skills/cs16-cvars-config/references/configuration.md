# Configuration pitfalls

## Bounds and binding

`create_cvar` takes `bool:has_min`, `Float:min_val`, `bool:has_max` and `Float:max_val`. An integer cvar can still have these Float bounds. Keep the bound variable global or static, match its type, and pass the documented capacity for a bound string.

When several cvars determine one cached result, bind their simple values and rebuild the result after configs finish and on relevant change hooks. A change hook receives text values; parse or retrieve typed values deliberately. Do not assume the relative ordering of hook notifications and binding updates when the algorithm can use `new_value` directly.

Cache pointers once after the owning module creates the cvar. A missing external cvar is a feature availability issue, not a reason to invoke a pointer native with `0`. Query `get_pcvar_bounds` only when its boolean result is true; an output parameter alone does not indicate that a bound exists.

## Generated configuration

Review `AutoExecConfig` and the config forwards in the target `amxmodx.inc`. The config can be buffered for execution before derived plugin state is initialized. Prefer `OnConfigsExecuted` for that state, and a cvar hook when live changes must update it afterwards. Reusing the same defaults in both a config file and a manual setter can override user choices unexpectedly.

Use namespaced plugin cvar names and the existing project's config layout. `FCVAR_*` flags affect engine behavior; use only those appropriate to the setting, and do not add visibility/security-related flags as decoration.

## Client cvar queries

`query_client_cvar` is asynchronous and returns text in its named callback, with any payload passed at registration. Read its exact prototype before implementing a handler. Retain userid/session information; revalidate it when the reply arrives. An empty, unavailable or unexpected response needs an intentional behavior. A client-supplied value is not authoritative server state.

## Gamedata lifecycle

Inspect `GameConfig` handle creation and each lookup's return convention. Missing offsets, empty keys and unresolved addresses are different failures. Treat them before using private data or registering a dependency that relies on them. Close an owned handle after the required lookups; document any reason to retain it.

For platform-sensitive pdata fallbacks, retrieve offsets from the project's maintained gamedata and inspect the selected pdata native's byte/cell/platform-difference conventions. ReAPI member access is preferred when it exposes the needed field.
