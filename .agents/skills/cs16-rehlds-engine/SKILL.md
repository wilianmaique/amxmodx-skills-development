---
name: cs16-rehlds-engine
description: Implement ReHLDS/ReAPI engine hooks, typed entity variables, usercmd/net data, sound/resource operations and modern user-message interception for a CS 1.6 server with the required engine API.
---

# ReHLDS engine and message APIs

Primary includes: `reapi_engine.inc`, `reapi_engine_const.inc`. Include through `<reapi>` after `<amxmodx>`. Some entity/model utility contracts live in this header without having the same capability requirement as an `RH_*` hook; verify the exact operation rather than inferring it from the file name.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md) and [ReAPI hooks](../cs16-reapi-hooks/SKILL.md) when using engine hookchains. Verify `is_rehlds()` before enabling ReHLDS-dependent functionality. Query exact declarations with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py).

## Typed engine data

- Prefer `get_entvar`/`set_entvar` with the documented `EntVars:var_*` field where that API fits the deployment contract. Scalars, strings and vectors have distinct variadic forms; read the field's get/set comments. Entity fields are engine state, not ReGameDLL private members.
- Use `get_ucmd`/`set_ucmd` with `UCmd` fields and the callback-provided usercmd handle. Use pmove, movevar and pmtrace APIs from the game header for their own contexts; do not treat these as persistent player fields.
- Use net-address and netchan APIs only with the correct object/index and `NetAdrVars`/`NetChan` selector. Do not guess pointer values or retain a borrowed network object beyond its valid context.
- In `RH_*` callbacks, read the selected enum's exact parameters and return type. Resource, authentication, packet, connection and sound hooks do not share a universal callback signature.

Read [engine contexts](references/engine-contexts.md) for lifetime-sensitive buffers and runtime-dependent behavior.

## Modern message interception

When the target ReHLDS/ReAPI exposes it, prefer `RegisterMessage` for message work needing pre/post interception, original data, recipient/destination edits or modification tracking. Use its `MessageHook:` handle and its matching enable/disable/unregister APIs.

Read [message protocol](references/message-protocol.md) before changing a message. These callbacks return `HC_*`; their data is accessed through `GetMessageData`/`SetMessageData`, not AMXX `get_msg_arg_*` or hookchain argument setters. AMXX `register_message` remains a supported fallback for a different server contract.

The [message observer example](assets/message-observer.sma) reads a checked `ArgString` through the modern protocol in post, retaining the matching `MessageHook:` handle.

## Sound emission

Prefer ReAPI's `rh_emit_sound2` over AMXX's `emit_sound` when the target server supports ReHLDS and the native is available. Use `emit_sound` when stock HLDS compatibility is required. Precache the sample with `precache_sound` and preserve channel, volume, attenuation, sound flags and pitch when migrating. Check the [recipient, origin and emission flag contract](references/engine-contexts.md#sound-emission) before choosing the added arguments.

With a valid emitting `entity` and the sample precached in `plugin_precache`, insert recipient `0` after the entity for untargeted emission.

```pawn
// Before:
// emit_sound(entity, CHAN_ITEM, "items/tr_kevlar.wav", VOL_NORM, ATTN_NORM, 0, PITCH_NORM);

rh_emit_sound2(entity, 0, CHAN_ITEM, "items/tr_kevlar.wav", VOL_NORM, ATTN_NORM, 0, PITCH_NORM);
```

## Other engine features

Use `rh_is_entity_fullpacked` for the documented per-host packing query. Choose separate APIs for line-of-sight and entity validation.

Map-name, pause, drop-client, realtime, visibility, bone/attachment, bodygroup and sequence helpers have individual contracts. `rh_set_mapname` is not an implicit map load. `rh_get_realtime` is a different time domain from game time; choose deliberately.

Compile against the project's ReAPI version and verify behavior with the actual engine API. Relevant cases include global versus single-recipient messages, other message hooks, changing connection state, invalid object contexts and paused-server timing.
