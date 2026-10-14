# Lifecycle and session-sensitive work

## Phase selection

| Requirement | Phase/API to inspect |
| --- | --- |
| Asset indices required by models, sounds, sprites or events | `plugin_precache`, the relevant `precache_*` native |
| Export a native or register a library for another plugin | `plugin_natives`, `register_native`, `register_library` |
| Register metadata, commands, cvars and regular hooks | `plugin_init` |
| Follow the project's existing earlier config phase | `plugin_cfg` |
| Derive state after all standard config files execute | `OnConfigsExecuted` |
| Create a plugin config with current cvars | `AutoExecConfig`; read its creation/execution semantics |
| Shutdown owned plugin resources | `plugin_end`; consider what can still be called during unload |

Verify exact phase guarantees in the target `amxmodx.inc`. Do not assume an event hook has already been registered inside precache, or that entities accessible during a later phase exist during startup.

## Client prerequisites

Use per-slot connection state, an authorization-ready flag and a put-in-server-ready flag when a feature needs both. Call a common initialization function from both forwards and have it run only once for that session. Copy an accepted auth ID; do not substitute IP or display name as a permanent account key by accident.

`client_disconnected` pairs with `client_connect`, including aborted connections. The entity remains valid at that point; messages and commands cannot reach the departing player. Save data from plugin-owned state, remove tasks and clear pending operations there. `client_remove` follows entity removal and is the phase where `is_user_connected` becomes false.

For delayed work, retain the initiating userid and, if needed, a plugin-managed session generation. Validate client range, connection state and that identity before writing slot arrays or performing game natives. A connected player in the same slot is not necessarily the player who started the operation. Apply the same rule to SQL callbacks, client cvar queries and `RequestFrame`, not only tasks.

## Tasks

Use an explicit task ID namespace if several features schedule independent per-player jobs. `remove_task` cancels the chosen namespace; it does not prove that an already-completed asynchronous operation belongs to the current occupant.

`set_task_ex` converts named flags to the underlying `set_task` contract. Pass the payload length appropriate to the actual array; match `(params[], task_id)` versus `(task_id)` to the registration. Repeating tasks need an intentional stop condition. For before/after-map timing, read the stock's flag mapping rather than assuming those options are ordinary delays.

Tasks execute on the game thread. File reads, blocking sockets and synchronous SQL still block there. Use the storage/network skill for asynchronous work or bounded processing.

## Filters and custom APIs

Optional dependencies require inspection of compiler module pragmas, `set_module_filter` and `set_native_filter`; suppressing a native error without providing a correct fallback leaves a broken feature. Use style-0 custom natives and validate each argument before obtaining arrays, strings or entity indices. Read the documented native error-reporting API if callers need actionable errors.
