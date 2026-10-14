---
name: cs16-entities-ham-fakemeta
description: Implement GoldSrc entity, virtual-function, trace and low-level engine work using HamSandwich, Fakemeta, engine and fun APIs when ReAPI does not cover the operation or a CS 1.6 plugin requires stock-server compatibility.
---

# Entities, Ham and Fakemeta

Primary includes: `hamsandwich.inc`, `ham_const.inc`, `engine.inc`, `engine_const.inc`, `engine_stocks.inc`, `fakemeta.inc`, `fakemeta_const.inc`, `fakemeta_stocks.inc`, `fakemeta_util.inc`, `hlsdk_const.inc`, `fun.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Retrieve exact declarations with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py), using the project's compiler include set. Prefer covered ReAPI semantic hooks/natives on a declared ReGameDLL/ReHLDS stack. These modules remain supported choices for uncovered engine/virtual operations, another game or required compatibility.

## Select the mechanism

- Ham hooks a game entity's virtual method. Read its `Ham_*` entry in `ham_const.inc` for forward parameters, execute parameters, return type and supported mods. Use `RegisterHamPlayer` for the player-class wrapper when appropriate; inspect its stock implementation for bot handling. Use `RegisterHam`/`RegisterHamFromEntity` for their actual class/entity contracts.
- Fakemeta forwards intercept engine/game-DLL functions through `FM_*`. Read `fakemeta_const.inc` for the exact function signature; use `FMRES_*` plus `forward_return` where a replacement result is required.
- The engine module supplies typed entity access, find/create/remove helpers, think/touch registration, trace/visibility, lights/camera and related services. Use `EV_INT_*`, `EV_FL_*`, `EV_VEC_*`, `EV_SZ_*`, `EV_ENT_*` with the matching accessor.
- `fun.inc` supplies direct general player gameplay natives. It is not automatically deprecated. Prefer a matching ReAPI semantic operation where supported, and keep fun where it satisfies the project's compatibility/operation contract.
- `engine_stocks`, `fakemeta_stocks` and `fakemeta_util` are implementations layered over lower-level calls. Read a stock's body before adopting it: an `fm_*` name does not guarantee a faster or more modern replacement for an existing native.

Read [entity and hook contracts](references/entity-and-hook-contracts.md) when hooking, executing or managing entity resources.

## Preserve validity and lifetime

Distinguish a valid edict from initialized private data and from a player of the current session. `pev_valid` has a documented private-data distinction; inspect it before calling Ham/pdata. A classname alone does not validate the entity's expected private layout.

Use `hlsdk_const.inc` for damage, flags, solid/movetype/render/channel/hull and related named constants. The same numeric value in a different enum family does not make the families interchangeable.

Owned trace handles created with `create_tr2` must be freed with `free_tr2` on every path. Trace handles passed by a hook are borrowed. Do not call an unrelated trace helper that replaces the current trace state before reading the result you need.

Register class-wide think/touch hooks once unless the API intentionally replaces an entity callback. Do not schedule redundant registrations per spawn. Validate targets inside callbacks, keep expensive I/O out of them and remove/disable plugin-owned work at its intended end.

## Private-data fallback

Prefer safe ReAPI members when exposed. If stock-server support needs pdata, read the exact get/set native and maintained project gamedata. Cell offsets, byte offsets and Windows/Linux/macOS differences are not universally interchangeable. Do not paste an unexplained numeric offset from another class or mod.

Compile and test the declared server/mod/bot path. Check pre versus post edits, original-call propagation, entity removal/reuse and recursion when executing hooked methods.
