---
name: cs16-reapi-hooks
description: Implement or migrate CS 1.6 ReAPI hookchains with exact RG/RH/RC callback signatures, correct pre/post argument and return handling, and explicit ReGameDLL/ReHLDS/addon capability requirements.
---

# ReAPI hookchains

Primary includes: `reapi.inc`, `reapi_version.inc`. Hook contracts are declared in `reapi_gamedll_const.inc`, `reapi_engine_const.inc` and `reapi_rechecker.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Include `amxmodx` before `reapi`. Verify the relevant subsystem before registration: `RG_*` requires ReGameDLL_CS, `RH_*` requires ReHLDS, and `RC_*` requires Rechecker. Preserve the include's version check.

## Register a precise hook

1. Retrieve the exact hook enum entry with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py) `show <hook-id>` against the project's compiler includes. Copy its documented parameter order and tags. The first parameter is often an entity index, but the selected entry decides that.
2. Select pre to change inputs, prevent the operation or replace its result; select post to observe the completed operation or its actual return. Do not choose post merely because a forum example uses it.
3. Register with `RegisterHookChain` and retain its `HookChain:` handle only when toggling is needed. Use `EnableHookChain`/`DisableHookChain` with that handle, not the enum function ID. Public callbacks must match the source contract.

## Arguments, original calls and returns

- `SetHookChainArg(number, AType:type, ...)` modifies inputs in pre. Numbering is one-based; count every documented argument, including the leading entity/`this`. The hook enum determines whether a value is Float, bool, string, vector, edict/class pointer or trace.
- `GetHookChainReturn` reads the original result in post; it has no effect in pre. Retrieve scalar versus string/vector results using the declared `AType` contract.
- To block a non-void original call, set an appropriate replacement with `SetHookChainReturn` before returning the intended `HC_*` action. The action controls dispatch, not the game function's typed return value.
- Prefer `HC_CONTINUE` when observing or editing arguments while allowing normal processing. Use `HC_SUPERCEDE` when the requested behavior requires suppressing the original. `HC_BREAK` and `HC_BYPASS` also skip other plugins; choose them only if that propagation is intentional. Read [dispatch semantics](references/dispatch.md).
- In post, use `IsReapiHookOriginalWasCalled` when the logic depends on the original having run. Another plugin can suppress it. Do not claim that a post edit retroactively changes inputs or undoes all original side effects.
- Avoid calling a hook-triggering semantic native recursively from the same hook. Inspect trigger/bypass behavior and use a narrow recursion guard or a controlled disabled handle where needed.

The [damage-scale example](assets/damage-scale.sma) changes argument 4 of `RG_CBasePlayer_TakeDamage` in pre and continues the original path. It intentionally permits valid world/environmental damage because it does not use attacker slot state.

## Migrate carefully

Prefer a matching game hook over message/log inference for gameplay. Preserve entity class, timing, bot behavior, original side effects and interaction with other plugins. Keep Ham/Fakemeta for uncovered hooks or required stock-server compatibility. ReAPI message hooks are a separate API: use [the engine skill](../cs16-rehlds-engine/SKILL.md), not `SetHookChainArg` on message data.

Compile against the declared ReAPI include version and test normal, blocked and reentrant paths. Report dependency changes explicitly.
