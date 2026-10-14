---
name: cs16-reapi-gameplay
description: Build or modernize CS 1.6 ReGameDLL gameplay with ReAPI player, weapon, inventory, economy, team, round, grenade and game-rules APIs and typed member access instead of inferred messages or hardcoded pdata.
---

# ReGameDLL gameplay

Primary includes: `reapi_gamedll.inc`, `reapi_gamedll_const.inc`, `cssdk_const.inc`. Include them through `<reapi>` after `<amxmodx>` so required regions, constants and safe member aliases exist.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md); read [the hook skill](../cs16-reapi-hooks/SKILL.md) if registering or replacing a call. Require `is_regamedll()` before enabling ReGameDLL features. Use [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py) against the target includes for exact native and selector contracts.

## Choose a semantic operation

- Players and inventory: prefer `rg_give_item`/`rg_give_custom_item`, slot removal/drop helpers, ammo/armor/defuse-kit helpers, `rg_round_respawn`, `rg_reset_maxspeed` and model/team helpers for covered operations. Inspect failure values; a failed grant can return `-1`.
- Money and game economy: prefer `rg_add_account` with the intentional `AccountSet` mode, and account-rule helpers when changing rewards. A direct `m_iAccount` write is not a money transaction or complete HUD update.
- Teams and rounds: use the team helper matching the requested join/swap/change behavior. Use semantic restart/end/win-check APIs and exact `WinStatus`/`ScenarioEventEndRound` constants. Read [players and rounds](references/players-and-rounds.md) before changing those transitions.
- Weapons and shooting: distinguish player backpack ammo, a weapon instance's clip/timing/mode state, global weapon info and `ItemInfo`. Read [weapons and damage](references/weapons-and-damage.md) for ownership, grant modes and prediction-sensitive changes.
- Custom entities: use `rg_create_entity`, supported find helpers, `SetThink`/`SetTouch`/`SetUse`/`SetBlocked`/`SetMoveDone` and `rg_remove_entity` when their ReGameDLL semantics fit. Retrieve callback prototypes and payload contracts before use. Removal is deferred by the game helper; do not reuse the entity as though destruction were immediate.

The entity create/find hash-table option is for known game entities. `rg_find_ent_by_class` explicitly cautions against custom classnames in this snapshot; choose a supported scan or owned entity registry for those classes. `SetThink` selects a callback; schedule the entity's next think through the documented state rather than assuming registration invokes it immediately.

The [spawn loadout example](assets/spawn-loadout.sma) grants a secondary slot item after successful player spawn and validates the item before setting backpack ammo.

## Use typed members deliberately

Read the chosen entry in `reapi_gamedll_const.inc` before every new variadic member access. Determine the entity class, `Member type`, `Get params` and `Set params`. Keep safe `get_member`/`set_member` aliases; reserve `MEMBER_UNSAFE` for a demonstrated need with verified class/layout.

Use `get_member_game`/`set_member_game` for `CSGameRules_Members`. Use the appropriate entity access for base/player/item/weapon/grenade/armoury/gib fields. Use `get_rebuy`/`set_rebuy` for rebuy state and the documented handle. Movement, movevars and pmtrace data have dedicated APIs and callback contexts.

Do not replace a complete game action with several member writes unless those side effects are intentionally being implemented. Team counts, item ownership/list links, animation state, HUD, win checks and observers can become inconsistent.

`cssdk_const.inc` supplies typed teams, weapons, slots, bullet/damage/animation/observer and game constants. Use the named value appropriate to the native. Do not assume a `CSW_*` value is a weapon entity or that a numeric cast creates a valid enum conversion.

## Validation

Compile with the project's includes and verify the changed game transition on its server stack. Relevant cases include bots, world damage, failed item grants, death/spawn order, observers, C4 ownership, repeated rounds and concurrent plugins. Keep messages in the presentation layer unless their exact wire behavior is the requested feature.
