# Mod boundaries and legacy contracts

## Day of Defeat

Use `dodconst.inc` for team/class/weapon values and `dodx.inc` for its event stage: team/class changes, spawn, scope, pickup, prone, weapon switch, grenade/rocket explosion, object pickup and stamina are separately declared forwards. `dodfun.inc` exposes gameplay manipulation; stats arrays and saved ranking queries come from `dodstats.inc`.

DoD weapon-list/body/model/score APIs have DoD semantics. Do not substitute a CS `TeamInfo` or weapon ID layout because the rendering looks similar. Validate a player versus a weapon entity according to the selected native.

## Team Fortress Classic

TFC goalitems, feign state, alliances and ammo banks are not CS inventory slots. `tfc_get_user_goalitem` has an output team parameter; `tfc_is_team_ally` compares teams, not client indices. The supplied `tfc_setpddata` exposes private-data configuration: inspect the maintained module/game data before using it, rather than guessing offsets from another mod.

`tfcstats.inc` and TFC event forwards are part of its stats module class. They share some names with other stats modules; inspect exact result sizes and event registration requirements for the actual deployment.

## The Specialists

Check `tsfun.inc` for declared weapon, ammo, powerup, stunt and time-control signatures. Some legacy forwards contain `UNAVAILABLE` parameters; a name alone does not describe a usable modern contract. Do not invent replacements or delete a parameter from a required callback without verifying the module.

The supplied `tsx.inc` labels `register_statsfwd` deprecated. TS version changes can remove supported virtual methods; `ham_const.inc` explicitly describes at least one TS 3.0 removal. Select only a method valid for that target/version.

## Natural Selection

NS separates game mode (`ns_is_combat`, `NSGameplay`), class/mask state, player/team resources, energy/jetpack fuel, experience/points, weapon properties and structures. Preserve the declared Float versus integer representation. `ns_get_user_team` includes a string output contract; it is not a copy of a CS enum getter.

`round_start`, `round_end(Float:roundtime)` and `map_reset` are NS forwards, not CS ReAPI hook IDs. Structure and particle functions use their own entity or `RawPS:`/`Particle:` handles. Read each creation/spawn/fire lifecycle; do not invent a generic AMXX destruction operation for those tags.

`ns_takedamage` is deprecated for the supplied module. When migrating to Ham, verify NS support, the entity class, damage signature, world/attacker inputs and whether hooks should run.

## ESF / EvolutionXCore

This supplied interface declares `#pragma library EvolutionXCore`. Its gameplay API uses mixed-case `getClient*`/`setClient*` symbols for power level, ki, health, speeds, protection/frozen/god and action queries. There is little parameter documentation beyond those declarations. Keep the exact names/types and determine the matching module/version before asserting units, ranges or semantics that the include does not state.

`esf_const.inc` supplies ESF-specific constants. These do not map automatically to CS teams/classes/weapon IDs. No ReAPI_CS helper should be proposed as a universal replacement for an EvolutionXCore operation.
