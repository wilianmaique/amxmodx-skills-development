# Modern API selection

The target include set and server capabilities decide availability. These preferences are grounded in the supplied declarations, not a blanket removal of older modules.

| Existing pattern | Preferred choice when supported | Behavior to preserve |
| --- | --- | --- |
| `client_disconnect` | `client_disconnected`; `client_remove` for after-removal work | Disconnect fires while the player entity remains valid; aborted connects are covered; network output is no longer deliverable |
| Letter flags in `register_event` | `register_event_ex` with `RegisterEventFlags` | Conditions, global versus single-recipient dispatch and documented alive/dead flag limitation |
| Letter flags in `set_task` | `set_task_ex` from `amxmisc` | Task ID, parameters, repeat count and before/after-map timing |
| Letter flags in `get_players` | `get_players_ex` / `get_playersnum_ex` | Bot/HLTV/alive/team filtering; no invented team enum conversion |
| `register_cvar` | `create_cvar` | Bounds and descriptions; an existing cvar retains its initial value |
| Repeated cvar name lookup | Cached `get_cvar_pointer` + `get_pcvar_*`, or `bind_pcvar_*` | Bound storage must be global/static and each variable binds to one cvar |
| Initialize derived settings in `plugin_cfg` | `OnConfigsExecuted` for values dependent on all executed configs | `plugin_cfg` remains valid for its existing phase; the later forward occurs once per map |
| Guess gameplay state from `HLTV`, `DeathMsg`, `CurWeapon`, log strings or repeated tasks | Matching `RG_*` hookchain or semantic `rg_*` native | Match the actual game phase; use messages for client presentation |
| Hardcoded pdata offsets for exposed ReGameDLL fields | Safe `get_member`/`set_member`, or `get_member_game`/`set_member_game` | Correct entity class, tags, array index and side effects; member writes do not perform a full game transition |
| Emulate a supported game operation with `fm_*`, `give_item`, direct member writes or manually sent HUD messages | Matching `rg_*` operation | Include handling, grants versus replacements, money tracking, HUD/model/team synchronization and win checks |
| Manual spawn/team/weapon polling | Matching semantic hooks; Ham/Fakemeta only where needed | ReAPI coverage, bot behavior, pre/post phase and recursion |
| AMXX `register_message` where richer original-data/post interception is needed | ReHLDS `RegisterMessage` when this version/runtime exposes it | AMXX uses `PLUGIN_*`; ReAPI message callbacks use `HC_*`; do not mix their data natives |
| `strbreak` | `argparse` or `argbreak` | Quoted arguments, cursor progress and truncation |
| `replace_all` | `replace_string` | Case matching, maximum buffer size and in-place behavior |
| `format` with independent input/output | `formatex` | Keep `format` when the destination is also a formatting input |
| `md5` / `md5_file` | `hash_string` / `hash_file` with `Hash_*` | Preserve digest algorithm and buffer size if a stored format depends on it |
| `geoip_code2`, `geoip_code3`, `geoip_country` | `_ex` variants | Failure returns and buffers; deprecated country-code functions can overflow on unknown IPs |
| `socket_change` | `socket_is_readable` | Timeout unit is microseconds; avoid positive waits on the gameplay thread |
| String regex flags where typed flags are appropriate | `regex_compile_ex` / `regex_match_all*` | Capture retrieval, match count and handle lifetime differ; do not blindly rename |
| `ArraySort` plus `ArrayGet*` inside every comparison | `ArraySortEx` when direct-element comparisons fit | Callback signature differs for cellsize 1 versus larger blocks |
| Obsolete DBI API | SQLX, using `SQL_ThreadQuery` for gameplay-driven queries | DBI field numbering/result semantics differ; callback query handles are borrowed |
| Global text vault for new keyed persistence | nVault or SQLX appropriate to the data model | Migrate stored keys and values; do not overwrite or reinterpret the old format silently |
| `read_file` repeatedly by line number | Stream with `fopen`/`fgets`/`fclose` | Existing text encoding, record boundaries and failure behavior |

## Hook families are separate protocols

| Family | Registration / data APIs | Callback action family |
| --- | --- | --- |
| ReAPI hookchain | `RegisterHookChain`, `SetHookChainArg`, `SetHookChainReturn`, `GetHookChainReturn` | `HC_*` |
| ReHLDS message | `RegisterMessage`, `SetMessageData`, `GetMessageData`, `GetMessageOrigData` | `HC_*` |
| Ham | `RegisterHam` / `RegisterHamPlayer`, `SetHamParam*`, `SetHamReturn*` | `HAM_*` |
| Fakemeta | `register_forward`, `get/set_tr2`, `forward_return` and operation-specific APIs | `FMRES_*` |
| AMXX event/message/command | `register_event_ex`, `register_message`, command registration and their own data APIs | The callback's documented `PLUGIN_*` or return contract |

Ordinary forwards such as `client_authorized`, CSX `bomb_*` and VTC speech callbacks are invoked by their modules; do not register them as ReAPI hooks. A void callback does not acquire a meaningful return value because another family supports one.

For a migration, describe the old trigger, selected replacement, dependency change and behavioral differences. If compatibility requires the old supported API, retain it deliberately and state the reason. Do not introduce ReAPI into a file-only or text-only plugin unless the requested feature benefits from it.
