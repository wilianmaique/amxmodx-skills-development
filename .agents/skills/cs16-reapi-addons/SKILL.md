---
name: cs16-reapi-addons
description: Integrate CS 1.6 ReAPI with Reunion client authentication metadata, Rechecker file-consistency queries and VoiceTranscoder speech/mute/audio APIs using exact addon contracts and availability guards.
---

# ReAPI addons

Primary includes: `reapi_reunion.inc`, `reapi_rechecker.inc`, `reapi_vtc.inc`. Include through `<reapi>` after `<amxmodx>`; those addon headers rely on parent definitions.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Retrieve exact definitions with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py). These are independent extensions: verify `has_reunion()`, `has_rechecker()` or `has_vtc()` before calling the corresponding APIs. Decide whether absence disables an optional feature or fails a plugin that explicitly requires it.

## Reunion

Use `REU_GetProtocol`, `REU_GetAuthtype`, `REU_GetAuthKey` and `REU_IsRevemuWithoutAdminRights` only for the requested metadata behavior. Preserve `client_auth_type` constants, including `CA_TYPE_STEAM`, and the supplied `is_user_steam` macro's meaning.

Do not invent `REU_*` natives from another version's documentation. The supplied authkey comment repeats parameter labels; trust the declaration and check same-version module implementation if the representation matters. Do not log auth keys as routine diagnostics or turn emulator/protocol metadata into an administrator permission without an explicit policy.

## Rechecker

Use `RegisterQueryFile` for registered file hash/availability requests and retain its `QueryFileHook:` handle for `UnRegisterQueryFile`. Its allowed request types are explicitly `RES_TYPE_EXISTS`, `RES_TYPE_MISSING` and `RES_TYPE_HASH_ANY`; other `ResourceType` values are not automatically valid request arguments.

For `RC_FileConsistencyProcess`, `RC_FileConsistencyFinal` or `RC_CmdExec`, read their hook enum parameter lists and use [ReAPI hook semantics](../cs16-reapi-hooks/SKILL.md). A consistency hook is not a generic AMXX forward. The `RegisterQueryFile` callback prototype is not fully declared in this snapshot; verify the matching module version's callback invocation before implementing it. Do not guess a signature based on an `RC_*` hook's parameters.

Relate deferred client results to a current session before applying state. Inspect whether a hash/absence result answers the requested condition; it does not alone establish arbitrary trust or automatically authorize punitive actions.

## VoiceTranscoder

Use `VTC_OnClientStartSpeak` and `VTC_OnClientStopSpeak` for speech transitions instead of polling every frame. Query speaking/muted state when needed; mute/unmute with the matching natives. Keep plugin-owned mute state coherent across disconnects and avoid undoing another feature's mute policy casually.

`VTC_PlaySound` sends a file through the voice stream; it is not a general engine sound emitter. Read its path/format requirements from the target addon implementation before accepting a new media format. Do not invent engine precache or voice file format guarantees from this short include.

For listener-to-sender permissions on ReGameDLL, inspect `rg_set_can_hear_player`, reset/query helpers or `RG_CSGameRules_CanPlayerHearPlayer`; those are a separate capability from VTC client mute state.

Compile and test with the declared addon versions. Verify absent-addon behavior, connect/disconnect, repeated speech transitions, query cleanup and the intended mute/receiver scope.
