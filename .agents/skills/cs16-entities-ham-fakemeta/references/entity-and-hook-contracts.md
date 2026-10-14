# Entity and hook contracts

## Distinct dispatch protocols

Ham uses `HAM_IGNORED`, `HAM_HANDLED`, `HAM_OVERRIDE` and `HAM_SUPERCEDE` with `SetHamParam*`, `GetHamReturn*` and `SetHamReturn*`. Fakemeta uses `FMRES_*` and its documented result APIs. ReAPI uses `HC_*`. Do not return one family's action from another family's callback.

Read both the forward and execute signatures in `ham_const.inc`. A method's callback can receive `this` as the leading entity, while arguments such as inflictor/attacker remain entities of their own. Use the method's declared parameter numbering when editing it. A return override is separate from the callback action, and post parameter changes cannot undo the executed original method.

`ExecuteHam` and `ExecuteHamB` differ in triggering hooks; `ExecuteHamB` explicitly retriggers them and can recurse. Inspect the selected operation before executing it from its own callback. Store the `HamHook:` registration handle for enable/disable calls; the `Ham_*` method ID is not a hook handle.

## Entity mutation

When creating an entity, check the documented result before setting its properties or calling spawn. Precache assets in startup, choose a valid classname/private class and apply keyvalues at the phase expected by the game's spawn behavior. An allocated edict alone may not be ready for virtual-method calls.

Origin and bounding-box changes can require relinking through the appropriate origin/size operation rather than arbitrary field writes. Preserve class/game initialization, collision/movetype and nextthink behavior required by the feature. Do not call spawn repeatedly as an attempt to fix an unrelated property.

Removed entity indices can be reused. In callbacks or deferred work, revalidate existence, expected identity/class and any plugin generation/marker. Avoid using an entity immediately after removing it; a semantic deferred removal API and an immediate engine removal API have different lifetimes.

## Traces and engine buffers

Use `create_tr2`/`free_tr2` for owned trace results. Read `TR_*` selectors with their actual scalar/vector/entity type. A hook trace handle, clientdata/entity-state/usercmd buffer or KeyValueData object is a borrowed object; use its own getter/setter family while that context is valid.

Fakemeta `engfunc` and `dllfunc` are variadic gateways; their generic declarations do not define the selected function's argument/return types. Read `EngFunc_*`/`DLLFunc_*` enum comments before calling. The same rule applies to engine stocks that wrap one of these calls.

## Pdata

`get_pdata_cbase`/`set_pdata_cbase` dereference private memory and require correct mod hamdata fields. `get_pdata_cbase` documents `-1` for a null result. Other pdata APIs can use different units and platform adjustments. Verify every such contract and the entity's private class before use. A valid field offset is not proof that the operation is a complete game transition.

If a desired Ham method is marked unsupported/deprecated for the actual mod, do not force registration by suppressing errors. Select a supported mechanism or explain that the requested hook is absent from that deployment contract.
