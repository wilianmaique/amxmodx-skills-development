# Statistics layouts and event semantics

Use `csstats.inc` as the layout authority. Each native documents its `stats`, `bodyhits`, name, authid, objective and rank outputs. Read its exact fixed array dimensions and return convention. `csstats_const.inc` defines objective indices rather than replacing all native-specific layouts with a single struct.

For common CSStats layouts, documented entries include kills, deaths, headshots, teamkills, shots, hits and damage; additional cells can carry rank information depending on the selected function. Never assume that an eight-cell array from a different query assigns its last cell the same meaning. Body hit arrays map the selected `HIT_*` values and have a generic/unassigned position.

Persistent ranking queries (`get_stats` and related calls) have their own index/next-result conventions. Read them before iterating; player slot IDs are not rank IDs. User, round, attacker, victim and weapon queries select different scopes. Check a native's success result before consuming outputs that may otherwise remain unset.

Objective arrays use `STATSX_TOTAL_DEFUSIONS`, `STATSX_BOMBS_DEFUSED`, `STATSX_BOMBS_PLANTED`, `STATSX_BOMB_EXPLOSIONS` and `STATSX_MAX_OBJECTIVE`. Map objective bits come from CSX `get_map_objectives` and represent available map objectives, not a particular player's completed objectives.

CSX `client_damage` reports an observed attack event with an integer stats damage value and team-attack marker. It is not equivalent to a mutable `RG_CBasePlayer_TakeDamage` Float argument. `client_death` reports observed death and teamkill metadata; returning a hook action from it does not prevent a death.

`custom_weapon_add` registers a stats weapon and returns a custom stats ID. `custom_weapon_shot` and `custom_weapon_dmg` feed that statistics system. Do not report an event twice through both a physical damage hook and manual stats recording if the module already observed it. Confirm the module's handling for genuinely custom damage paths.

The stats module class can auto-resolve to CSX for CS. Verify actual module availability and configuration when a feature needs saved rankings; the presence of `csstats.inc` alone does not mean persistent stats are enabled.
