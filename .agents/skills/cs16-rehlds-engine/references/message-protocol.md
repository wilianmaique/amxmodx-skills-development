# ReHLDS message protocol

The supplied ReAPI engine include exposes `RegisterMessage(msg_id, callback, post)` and a separate `MessageHook:` handle family. The callback parameters are `(msg_id, msg_dest, msg_entity)`, and its dispatch action belongs to `HC_*`.

## Data selection

Read the `MsgDataType` and `MsgArgType` entries in `reapi_engine_const.inc`. `MsgDest`, `MsgMsgId`, `MsgOrigin`, `MsgTargetId` and `MsgArg` select different data. The supplied modification-tracking native comments mention `MsgIndex`, but the actual selector enum declares `MsgMsgId`; use the declared constant. A `MsgArg` operation also needs the argument's one-based index; strings/vectors require output/value arrays and documented lengths. Validate argument count and type before accessing content.

`GetMessageData` reads current data. `GetMessageOrigData` reads the original captured data. `SetMessageData` changes the message before original processing. Do not infer that editing data in post can unsend a delivered packet.

Keep this API separate from AMXX `get_msg_arg_*`, `get_msg_args` and `set_msg_arg_*`. Those operate in AMXX `register_message` context. `SetHookChainArg` operates in ReAPI function hookchains, not this message data context. Coinciding callback argument names do not join the protocols.

## Original data and other plugins

`IsMessageDataModified` and `ResetModifiedMessageData` can operate on all data or a selected part/argument. Reset only the portion the requested feature owns; resetting `MsgAny` may remove other plugins' intentional modifications. Prefer `HC_CONTINUE` for inspection or edits that preserve dispatch.

`SetMessageBlock`/`GetMessageBlock` use `MsgBlockType`, not AMXX's message block constants by assumption. Read whether the selected block affects one occurrence or ongoing delivery. When enabling a persistent block, define when it is removed.

Cache user-message IDs after they have been registered and distinguish them from `SVC_*` engine message IDs. Preserve receiver and destination rules for `MSG_ONE*`, broadcast and PVS/PAS messages. A recipient index of `0` does not universally mean a valid individual recipient.

## Handles and compatibility

Store the `MessageHook:` value returned by `RegisterMessage` if toggling or unregistering is necessary. Never pass a `HookChain:` handle or message ID to `UnregisterMessage`.

Use this richer API when both the compiler includes and runtime expose it. If supporting stock HLDS or an older ReAPI, use the explicitly supported AMXX message path or a deliberate capability-specific feature choice. A function name found in a newer snapshot does not create it in an older deployed module.
