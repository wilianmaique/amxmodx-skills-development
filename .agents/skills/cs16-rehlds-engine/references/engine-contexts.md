# Engine contexts and borrowed objects

Entity variables are per-edict engine state. ReGameDLL members are private game objects. PlayerMove, MoveVars, PMTrace and UserCmd represent separate structures with context-dependent availability. Inspect the exact hook and selector comments before reading or writing one.

`get_key_value`, `set_key_value` and buffer variants require a valid provided engine info buffer. A client index or an arbitrary integer is not the buffer pointer. Copy values while the callback owns that context; do not save the pointer into deferred work.

`get_netadr`/`set_netadr` and `get_netchan`/`set_netchan` require their documented address/object/index input. Network fields may include scalars, strings and arrays. Treat their types as declared by the selector, including maximum lengths and valid address families. Deprecated GoldSrc IPX enum entries are not modern networking choices.

For connection hooks, distinguish a client not yet put in server from an active player. A valid network object does not imply that player private data is initialized. Use the callback's documented rejection/drop path and preserve a useful reason where the task changes admission behavior.

Sound/resource operations require precached assets and appropriate engine context. `rh_emit_sound2` can target recipients and provides custom emission/origin flags; inspect those rather than assuming it is a direct replacement for every `emit_sound` call. Do not equate an entity being fullpacked for one host/frame with current visibility, valid private data or transmission to every player.

`rh_get_realtime` measures engine realtime. `get_gametime` follows gameplay/map time. Do not combine deadlines from those clocks unless conversion is explicit. Pause-sensitive features need a chosen clock rather than an arbitrary preference for the newer function.
