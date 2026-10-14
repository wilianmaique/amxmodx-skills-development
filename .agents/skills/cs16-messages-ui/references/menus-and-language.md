# Menus and language

## Ownership

A `menu_create` handle is owned by the plugin. For a menu built per invocation, destroy it on selection and every documented exit/cancel/timeout path. For a shared menu, retain it until no client/feature needs it; do not apply the per-invocation destruction pattern blindly.

Inspect `menu_item_getinfo` after validating `item >= 0`. The item info string can store a stable action/key while the display text is localized. Revalidate client session, permission and target state at selection time; the world can change while a menu is open.

`menu_cancel` may invoke the menu handler; inspect the current handle and avoid double destruction during disconnect cleanup. Track plugin-owned menus when cleanup can overlap a selection. Do not assume every negative item value means an ordinary selected item.

Read `MPROP_*` for their typed values and ignored/deprecated properties. Automatic pagination and reserved exit/back/next keys are part of newmenus behavior; a manual key bitmask from old menus does not directly describe a newmenus item index.

## Localization

Use `register_dictionary` for maintained dictionary files. Format per-client labels with `%L`, the client language target and the correct key arguments. A shared already-formatted menu title may show one client's language to another; create per-language/per-client display state if that feature requires it.

`SetGlobalTransTarget` changes implicit translation state; explicit `%L` targets are often clearer when formatting for multiple recipients. If the project uses `%l`, verify its implicit-target behavior in the current include/compiler/module combination rather than mixing it with `%L` arguments.

`CreateLangKey`, `GetLangTransKey`, `AddTranslation` and `LookupLangKey` have specific key/lookup contracts. Read their signatures before dynamically registering or looking up phrases; do not invent a destruction API for `TransKey`.

Treat text lengths according to the selected formatting/message native, including UTF-8 boundaries where supported. The string skill provides multibyte helpers when ordinary byte-wise truncation is inappropriate.
