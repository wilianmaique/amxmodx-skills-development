# Players, economy, teams and rounds

## Player actions

Choose a native by its complete behavior. `rg_set_user_team` sets team/model without killing the player; its `send_teaminfo` and `check_win_conditions` options have independent effects. `rg_join_team`, `rg_switch_team`, `rg_swap_all_players` and balancing are different transitions. The supplied `RG_CBasePlayer_SwitchTeam` note does not promise to catch every manual team change; find the hook that matches the actual transition.

Do not treat `m_iTeam` assignment as a team-change transaction. For a multi-player rebalance, determine when player counts/win conditions must be recalculated instead of triggering intermediate checks for every write. Preserve the intentional alive/dead, observer and team-model state.

`rg_add_account` distinguishes `AS_ADD` and `AS_SET`. Choose whether to track the displayed change. Altering a reward rule affects a shared rules policy, while altering an individual account affects one player. Read the selected `RewardRules` constant before changing shared economy behavior.

Spawning through `rg_round_respawn` performs a game transition. Setting health, clearing a dead flag or manually sending a spawn-like message is not equivalent. A post-spawn loadout should validate that the original ran and the player is alive; pre-spawn grants can be removed by default spawn equipment.

Movement speed may be reset by weapon/deploy/round logic. Use the matching reset/maxspeed hook and semantic native when implementing a persistent speed policy. `var_maxspeed` writes by themselves do not guarantee persistence across those transitions.

## Rounds and objectives

`rg_round_end` takes a Float delay, `WinStatus`, `ScenarioEventEndRound`, message, sentence and trigger flag. The trigger flag controls hookchain invocation and can recurse. Choose an event matching the intended objective; do not substitute a generic winner constant for a scenario event.

Distinguish round commencement, round restart, freeze end, round end and map cleanup. `RG_CSGameRules_RestartRound`, `RG_CSGameRules_OnRoundFreezeEnd`, `RG_RoundEnd` and related hooks run at different stages. Use `get_member_game` for rules observation and a semantic native for the actual transition.

C4 planting, transfer and defusing depend on owner/team/game state. Inspect `rg_plant_bomb`, `rg_transfer_c4`, bomb-state queries and the `RG_CGrenade_DefuseBomb*` hooks rather than reconstructing a bomb from a visible model or a message. Track a bomb entity as an entity, not as a weapon ID.

## Observers and death

`rg_set_observer_mode` and `rg_observer_find_next_player` require a valid observer, including the documented `PFLAG_OBSERVER` state. Validate that prerequisite rather than checking only `!is_user_alive`.

`rg_death_notice` emits game notice/log/win-check behavior; `rg_send_death_message` supplies message details including assister, flags and kill rarity. A death message alone does not perform the victim's death transition. Use the appropriate killed/damage path for gameplay changes and the presentation helper for presentation.

Find exact player and game-rules members on demand through the source catalog. The large member enum is a typed contract, not a list of fields that can be freely assigned at any time.
