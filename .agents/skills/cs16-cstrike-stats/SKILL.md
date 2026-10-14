---
name: cs16-cstrike-stats
description: Use CS 1.6/CZ CStrike gameplay interfaces, CSX bomb/grenade/damage/death forwards and CSStats player/weapon/objective statistics; preserve stock-server compatibility and migrate covered gameplay to ReAPI where supported.
---

# CStrike, CSX and statistics

Primary includes: `cstrike.inc`, `cstrike_const.inc`, `csx.inc`, `csstats.inc`, `csstats_const.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Retrieve declarations with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py), filtering by include because `client_damage`, `client_death` and `get_user_stats` names also occur in other mods.

## CStrike gameplay

Use `cs_*` APIs deliberately for stock CS/CZ compatibility or a feature they expose. These APIs are supported, not universally deprecated. On a declared ReGameDLL deployment, prefer a matching semantic `rg_*` operation when it maintains the intended game transition.

- Preserve `CsTeams`, `CsInternalModel`, `CsArmorType`, `CsWeaponInfo`, `CsWeaponClassType` and relevant map-zone/zoom constants from the target header.
- Player backpack-ammo and weapon-entity clip/mode functions accept different identifiers. Resolve `cs_get_user_weapon_entity` for the active item, validate it, then use weapon-entity APIs. Do not pass `CSW_*` where an entity is expected.
- Read team/model, deaths/scoreboard, VIP, defuse/plant, zoom, silencer/burst, armoury and hostage setters for synchronization flags and valid target classes. A HUD message does not replace the game state update.
- Entity creation/find/class helpers may implement a maintained classname hash. Use the native appropriate to the same runtime rather than changing a classname through an unrelated field write and leaving a lookup index stale.

## CSX event observation

`client_damage`, `client_death`, `grenade_throw` and `bomb_*` are module forwards. Implement their declared public callbacks; do not register them as ReAPI hook IDs. They observe events after the stated stages and do not supply a pre-damage replacement return.

Use matching ReAPI hooks for modifying gameplay. Keep CSX callbacks for stats/notifications or the compatibility contract. Avoid processing the same kill or grenade twice by attaching both observer paths without a reason.

Custom weapon stats use IDs returned by `custom_weapon_add`, separate from a live weapon entity. `custom_weapon_dmg` records a stats event; it is not a native that applies physical damage. The supplied comment mentions a `client_kill` callback, while the declared death forward is `client_death`; resolve disputed callback behavior against the matching module implementation before relying on that comment.

## Statistics

Read [statistics layouts](references/statistics-layouts.md) before interpreting arrays, ranks or objective counts. Size and meaning come from the selected native, not from a guessed generic stats struct. Use `STATSX_*` objective constants and `MapObjective` bits for the corresponding API.

Distinguish session, round, attacker/victim, weapon and persistent ranking statistics. Check result conventions for missing users/ranks; preserve rank iteration and reset semantics. Other mod stats headers are not substitutes for CSStats just because the native names match.

Compile and verify any changed synchronization or stats accounting. Relevant cases include unranked clients, bots, custom weapons, repeated rounds, teamkills and observer callbacks firing after the actual game event.
