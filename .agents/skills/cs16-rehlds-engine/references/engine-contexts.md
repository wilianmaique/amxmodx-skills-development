# Engine contexts and borrowed objects

Entity variables are per-edict engine state. ReGameDLL members are private game objects. PlayerMove, MoveVars, PMTrace and UserCmd represent separate structures with context-dependent availability. Inspect the exact hook and selector comments before reading or writing one.

`get_key_value`, `set_key_value` and buffer variants require a valid provided engine info buffer. A client index or an arbitrary integer is not the buffer pointer. Copy values while the callback owns that context; do not save the pointer into deferred work.

`get_netadr`/`set_netadr` and `get_netchan`/`set_netchan` require their documented address/object/index input. Network fields may include scalars, strings and arrays. Treat their types as declared by the selector, including maximum lengths and valid address families. Deprecated GoldSrc IPX enum entries are not modern networking choices.

For connection hooks, distinguish a client not yet put in server from an active player. A valid network object does not imply that player private data is initialized. Use the callback's documented rejection/drop path and preserve a useful reason where the task changes admission behavior.

An entity being fullpacked for one host and frame describes packing for that host. Check visibility, private-data validity or delivery to other players through the APIs for those operations.

`rh_get_realtime` measures engine realtime. `get_gametime` follows gameplay/map time. Do not combine deadlines from those clocks unless conversion is explicit. Pause-sensitive features need a chosen clock rather than an arbitrary preference for the newer function.

## Sound emission

`rh_emit_sound2` takes `recipient` immediately after `entity`. Pass `0` as the recipient for untargeted emission or a client index to target one listener. `entity = 0` selects worldspawn and allows an explicit `origin`. Check the existing emitter and audience when migrating calls that pass `0` to `emit_sound`.

The `emitFlags` argument takes `SND_EMIT2_*` constants. Use `SND_EMIT2_NOPAS` only when the sound should bypass potentially audible set (PAS) filtering. Check the return value when subsequent behavior depends on successful emission.
