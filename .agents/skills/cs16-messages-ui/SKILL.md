---
name: cs16-messages-ui
description: Build CS 1.6 AMXX user-message and temporary-entity presentation, HUD/chat output, newmenus interfaces and multilingual text with exact wire schemas, recipient rules and menu ownership.
---

# Messages, menus and translations

Primary includes: `messages.inc`, `message_const.inc`, `message_stocks.inc`, `newmenus.inc`, `lang.inc`. HUD/chat helpers also live in `amxmodx.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Query the selected native, `TE_*` message schema, menu property and language contract with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py).

## Message mechanism

Use a semantic game native to change gameplay state where available, and messages to present it. For richer ReHLDS interception, prefer `RegisterMessage` when the compiler/runtime supports it and read [the engine message protocol](../cs16-rehlds-engine/references/message-protocol.md). AMXX `register_message` is the supported AMXX-context path and returns `PLUGIN_*` actions.

Within AMXX message callbacks, use `get_msg_args`, `get_msg_argtype` and matching get/set argument natives. Argument numbers are one-based. Read the actual message schema before changing type/value/order. Do not mix these APIs with ReAPI `GetMessageData` or hookchain setters.

Cache user-message IDs after registration. Distinguish those IDs from `SVC_*` engine messages and `TE_*` submessage types. Read [presentation contracts](references/presentation-contracts.md) for destinations, message pairing and recursion.

## HUD, chat and menus

- Prefer purpose-built HUD/chat helpers over assembling equivalent packets when they cover the requested presentation. Choose recipients deliberately; cache synchronization HUD objects when the feature needs channel management.
- Use `newmenus` for new interactive menus. Keep item info stable and separate from localized display labels. Handle negative cancellation/exit/timeout values before looking up an item; do not immediately redisplay a cancelled menu inside its handler.
- Distinguish a shared persistent menu from a per-request menu. Destroy each owned menu exactly once at its intended end, including exit paths; do not destroy a shared handle still displayed to another client.
- Use documented menu properties and callback contracts. Avoid deprecated no-effect properties such as `MPROP_ORDER` and `MPROP_PADMENU`. `menu_create`'s `ml` argument should be interpreted according to the target include, not assumed to provide automatic localization.

Read [menus and language](references/menus-and-language.md) for concurrent users and localization.

## Localization

Register dictionaries, select a valid client/server language target and use `%L` with an explicit recipient when formatting per-player text. The target is part of the formatting arguments; a translation key alone is not enough. Query dynamic language keys/translations through their `TransKey:` APIs if the feature needs them.

Escape or format untrusted display text as data. A player's name or a config string must not become the format string. Keep protocol lengths and Pawn string capacity distinct.

Compile and test receiver scope, schema correctness, menu cancellation and two clients using different languages concurrently. Verify presentation changes without relying on them as proof of game-state mutation.
