# Weapons, item state and damage

## Identity and ownership

A `WeaponIdType:WEAPON_*` identifies a weapon type. A `weapon_*` classname identifies a spawn/grant class. A weapon entity index identifies a particular item instance. Resolve its documented owner/player member before using player APIs; never pass a weapon ID as an entity index.

Read `m_pActiveItem`, `m_rgpPlayerItems`, weapon/player links and their get/set signatures if traversing inventory. Array slots are not interchangeable with weapon IDs. Prefer supported find/slot helpers to editing linked-list pointers.

`rg_give_item` returns an item entity or `-1`. `GT_APPEND`, `GT_REPLACE` and `GT_DROP_AND_REPLACE` have different inventory effects. Validate the result before accessing weapon members. Decide whether a replacement should remove or drop an existing slot and whether to retain its ammo.

Use player ammo helpers for backpack/type ammo and the documented weapon instance member or semantic helper for its clip. An ID-based current-weapon ammo helper may have a different selection contract; inspect it rather than guessing.

## Per-instance versus shared info

- `get_member`/`set_member`: state of a specific weapon instance (clip, mode, timing, reload state and class-specific members).
- `rg_get_weapon_info`/`rg_set_weapon_info`: shared weapon metadata through `WpnInfo`; selectors have their own get/set forms and writable restrictions.
- `rg_get_iteminfo`/`rg_set_iteminfo`: the item's `ItemInfo` fields.
- Global `ItemInfo` helpers: shared item-info array by weapon ID. Client ammo/HUD limits depend on when `WeaponList` is sent; the include documents applying global changes before that message or resending it when necessary.

Updating shared metadata affects more than one player/item. Restore or retain it according to the requested plugin lifetime; do not silently change global limits for a temporary individual effect.

## Weapon actions

Prefer `rg_weapon_deploy`, `rg_weapon_reload`, `rg_weapon_shotgun_reload`, `rg_weapon_send_animation`, `rg_weapon_kickback`, switching and instant-reload helpers when they express the intended behavior. Model indices/assets must be precached. Animation, owner prediction, clip/state and next-attack timing remain coupled; changing only a visible model or one timer can desynchronize them.

Use class-specific members only on matching entities. The safe member variant checks the class relationship; it does not guarantee that every arbitrary sequence of valid writes produces a valid weapon state.

## Damage and traces

`RG_CBasePlayer_TraceAttack` and `RG_CBasePlayer_TakeDamage` represent different stages. Choose the stage that matches hitgroup/tracing versus applied damage. In the supplied TakeDamage contract, argument 4 is `Float:flDamage`; scaling it in pre and returning `HC_CONTINUE` preserves the original processing path.

Attacker/inflictor can be world `0`, a grenade, another entity or a player. Validate player membership before reading a per-player array; do not discard valid environmental damage merely because attacker is not a player.

For multidamage, inspect clear/add/apply helpers as one lifecycle. Preserve inflictor/attacker distinctions. Use named `DMG_*`, `Bullet`, hull and trace flags appropriate to the function. The array-return signature of `rg_fire_bullets3` is `Float:[3]`; compile its use instead of treating it as a scalar Float result.

Create owned traces only with their matching API and free them. A trace borrowed from a hook is callback-owned. Grenade spawning and weaponbox creation have documented null/failure sentinels and ownership requirements; inspect them before attaching or removing items.
