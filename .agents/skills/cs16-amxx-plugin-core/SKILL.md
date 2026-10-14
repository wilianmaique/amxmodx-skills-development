---
name: cs16-amxx-plugin-core
description: Implement or review AMX Mod X Pawn plugin lifecycle, client sessions, commands, tasks, permissions and custom native/forward interfaces for CS 1.6 and compatible GoldSrc plugins.
---

# AMXX plugin core

Primary includes: `amxmodx.inc`, `amxconst.inc`, `amxmisc.inc`, `amxmodx_version.inc`, `core.inc`.

Read the [shared contracts](../cs16-api-reference/references/shared-contracts.md) and query exact signatures through [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py). Use the project's actual compiler includes. `amxmodx.inc` transitively includes many utility headers; additional module dependencies should follow the features used.

## Lifecycle and client state

- Register plugin metadata, commands, cvars and stable hooks in `plugin_init`. Register exported natives/libraries in `plugin_natives`. Precache required assets in `plugin_precache`; do not lazily precache new models/sounds after startup.
- Use `OnConfigsExecuted` for initialization based on fully executed server, AMXX, plugin and per-map configs. `plugin_cfg` is an earlier valid phase, not a guarantee that those configs have all executed. Read [lifecycle and sessions](references/lifecycle-and-sessions.md) when work depends on startup order.
- Prefer `client_disconnected(id, bool:drop, message[], maxlen)` over deprecated `client_disconnect`. Its player entity is still valid, but output will not reach the client. Use `client_remove` for after-removal work.
- Treat `client_authorized(id, const authid[])` and `client_putinserver(id)` as independent prerequisites. Authorization may occur first or second; bots use `BOT`. Reset slot data for every new session and cancel per-client work on disconnect.
- Revalidate userid/generation before delayed work uses a saved client index. Prefer session payloads to relying on a task ID alone. The [session-task example](assets/session-task.sma) shows task cancellation plus userid verification.

## Modern commands, events and scheduling

- Prefer `register_event_ex`, `set_task_ex`, `get_players_ex` and `get_playersnum_ex` when this include set supports them; use their named `RegisterEventFlags`, `SetTaskFlags` and `GetPlayersFlags`. The `_ex` task/player helpers are stocks in `amxmisc.inc`.
- Use `RequestFrame` when the requested timing is explicitly the next frame. It is a one-shot callback, not a substitute for a timed repeating task. Copy needed session data; callback context does not preserve a borrowed engine pointer.
- Choose `register_clcmd`, `register_concmd` or `register_srvcmd` by who may invoke the command. Account for console id `0`. In admin handlers, use `cmd_access`, and use `cmd_target` with appropriate `CMDTARGET_*` rules for target resolution and immunity.
- Use named `ADMIN_*` permissions and `PLUGIN_*` actions belonging to the callback contract. Do not return `HC_*`, `HAM_*` or `FMRES_*` from an AMXX command callback.
- Prefer a semantic game hook for gameplay logic where ReAPI provides one. Keep AMXX user-message events and log events when their presentation or log semantics are the intended trigger. Read [modern API selection](../cs16-api-reference/references/modern-api-selection.md) for migration decisions.

## Inter-plugin APIs

Use `register_native(..., style = 0)` and the `get_param`/`get_string`/`set_*` parameter APIs in a public `(plugin_id, num_params)` handler. Check parameter count and target state. Publish clear ownership, return and error contracts. Do not use deprecated style 1 or `param_convert` for new interfaces.

For public forwards, read `CreateMultiForward`/`CreateOneForward`, `ExecuteForward`, `PrepareArray` and `DestroyForward` together. Distinguish the native's execution result from the callback result passed by reference; select the documented `ET_*` aggregation and `FP_*` types. Do not cache prepared array tokens beyond the documented execution context.

`core.inc` exposes low-level argument and runtime helpers; use them only when the actual task needs varargs/runtime introspection. Preserve diagnostics instead of concealing missing modules with obsolete `plugin_modules`/`require_module` APIs.

## Check the result

Compile against the selected AMXX version, then exercise the changed lifecycle/command/deferred behavior. Relevant cases include console invocation, denied permissions, target ambiguity, authorization order, disconnect before callback and reused client slots. Read only the source contracts required by the change.
