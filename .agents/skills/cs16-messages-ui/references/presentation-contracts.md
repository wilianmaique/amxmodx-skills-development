# Presentation contracts

## Destinations and pairing

`message_begin` and `message_begin_f` differ in origin representation. Use the declared `MSG_*` destination and a valid recipient for single-client messages; use the appropriate origin for PVS/PAS destinations. Pair a begin with the matching end and preserve the selected sequence of `write_*` operations.

`message_const.inc` documents temporary-entity wire layouts, often directly below each `TE_*` constant. Read that layout before emitting bytes, shorts, coordinates, strings or model indices. Do not substitute an integer coordinate writer for a Float writer or change field widths because the Pawn source type appears similar.

Required sprites/models/sounds must be precached before use. A plugin-local resource path is not its wire index. Bound byte/short fields to their intended format; a large integer may serialize differently from the intended visual value.

## Interception and recursion

AMXX `register_message` operates before delivery and has its own callback prototype `(msg_id, msg_dest, msg_entity)`, argument natives and `PLUGIN_*` results. Its raw message data and AMXX event `read_data` APIs are different callback contexts. Validate count/type before reading optional fields.

The `emessage_*`/`ewrite_*` family goes through Metamod's message path; ordinary and intercepted message paths have different propagation. Read the native notes before emitting from a message callback. Sending the same message through a hook-triggering path can recurse. A direct rewrite of the current message often avoids unnecessary re-emission when the requested behavior fits.

Use `set_msg_block` with the selected AMXX block constant only when intentionally blocking that message and scope. ReAPI uses `MsgBlockType` and a different API. A permanent block needs an intentional restoration/lifetime policy; it is not equivalent to returning handled once.

For gameplay messages such as money, team, weapon list or death notices, verify whether the game native already sends the required packet. Do not duplicate it or alter client presentation while leaving the underlying game state inconsistent.
