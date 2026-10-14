# ReAPI dispatch semantics

The supplied `reapi.inc` defines these actions:

| Action | Dispatch meaning |
| --- | --- |
| `HC_CONTINUE` | Continue normal processing |
| `HC_SUPERCEDE` | Skip the original function and use the selected replacement return |
| `HC_BREAK` | Skip the original and remaining forwards; use the selected replacement return |
| `HC_BYPASS` | Call the original while skipping remaining forwards; in pre, subsequent post forwards are also skipped |

Treat these as ReAPI protocol values. `PLUGIN_HANDLED`, `HAM_SUPERCEDE` and `FMRES_SUPERCEDE` belong to other protocols, regardless of coincidentally equal numeric values.

## Replacement returns

Read the hook's `Return type` comment. A CS BOOL/int result can require `ATYPE_INTEGER`, while an explicitly bool return uses its documented type. Entity/class-pointer results and string/vector results need the corresponding `ATYPE_*` representation. Do not apply a blanket boolean convention to every hook.

For a void original, there is no invented scalar result to return. Suppression still needs the correct dispatch action. For an original that allocates/grants/removes something, reproducing only its return value does not reproduce its side effects; prefer argument editing or a semantic native when that preserves the intended behavior.

`SetHookChainArg` does not change the Pawn callback's already-received parameter variable. If later code in the same callback needs the changed value, also keep it in a local variable. Getters for original returns are post-context operations; do not use their value in pre as though the original had executed.

## Hook scope and reentrancy

Register a class-specific `RG_*` hook only on the ReGameDLL stack that provides it. For example, weapon hooks receive weapon entity indices, not their owners. Resolve an owner through the documented member and validate it before accessing player state.

Calls like `rg_round_end(..., trigger = true)` explicitly retrigger hookchains and can recurse. Check the selected native's behavior rather than assuming every `rg_*` call bypasses or triggers hooks the same way. Keep a recursion guard scoped to that operation and release it on every path.

After another plugin supercedes an original, post callbacks may still run. Check `IsReapiHookOriginalWasCalled` before relying on newly initialized state or an original return. Disable/re-enable handles only when the operation truly needs it, and avoid suppressing unrelated plugins with `HC_BREAK`/`HC_BYPASS` for routine observation.

For uncertain pointer/trace argument representations, read the hook entry and corresponding version's module implementation. Borrowed engine objects remain callback-scoped; copying an integer pointer into a task does not extend their lifetime.
