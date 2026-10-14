# Shared implementation contracts

Read this once for a CS 1.6 plugin task, then read only the domain references needed by that task.

## Project environment

When selecting local compile inputs, read the project's established toolchain notes (by default `.agents/cs16-environment.md`) and relevant build configuration. Reuse recorded compiler/include paths after checking the paths needed by the task. If the selection is missing or stale, follow [project toolchain memory](project-environment.md) to discover and persist the established environment in the consuming project. Keep these machine/project settings outside the portable skills, and preserve existing user instructions. A known include path is sufficient for API lookup when compilation is not needed.

## Source and deployment contract

- Treat the target project's include directory and build command as the compile contract. The bundled 76-file snapshot is a reference baseline. If both exist, query the target set with `--include-dir`; do not combine symbols from different versions.
- Record the game (CS 1.6/CZ or another GoldSrc mod), AMXX compiler/module versions and required subsystems. Including `reapi` does not establish that ReHLDS, ReGameDLL_CS, Reunion, VTC or Rechecker is available.
- A hard ReAPI dependency is appropriate when the requested plugin targets it. After ReAPI loads, check `is_regamedll()` for game hooks and `is_rehlds()` for engine hooks before registering the affected feature. `has_reunion()`, `has_vtc()` and `has_rechecker()` guard their respective extension calls. These functions cannot rescue a plugin that failed to load because ReAPI itself is absent.
- Build an optional missing-module path only when the project's compatibility contract needs one. AMXX's include pragmas and native resolution must be handled as well as runtime branching; a conditional around a native call alone is insufficient. Consult `set_module_filter`, `set_native_filter`, `LibraryExists` and their exact callback rules before implementing that path.
- Preserve `__reapi_version_check`. It checks the include API major and minimum minor against the module. Do not remove it to hide a mismatch or invent an exact release requirement from an include filename.

## API choice

Prefer a semantic API that performs the intended game transition and maintains its side effects. ReAPI hookchains and `rg_*` helpers are preferred for covered ReGameDLL operations; ReHLDS hooks and supported modern message interception are preferred for covered engine work. Use Ham, Fakemeta, engine, CStrike or fun where the operation is uncovered, another mod requires them, or the server contract requires a supported fallback.

Newer names alone do not establish equivalence. Check timing, original-call behavior, return type, HUD updates, win checks, team counts, bot support and inter-plugin propagation. Presentation events and CSX statistics callbacks remain useful for their own purpose even when gameplay is controlled through ReAPI.

## Pawn and identifiers

- Preserve `Float:`, `bool:`, handle and enum tags. `Float:integer` reinterprets cell bits; `float(integer)` converts a number. Do not remove tags just to silence a mismatch.
- Most writable string APIs take capacity excluding the terminator: use `charsmax(buffer)` unless that native documents a different contract. Some regex, JSON, file, raw-byte and container parameters describe size differently; read the selected function.
- Distinguish player indices, entity indices, weapon IDs, classnames, item instances, module handles and borrowed engine pointers. `WEAPON_*`, `CSW_*`, `TeamName`/`TEAM_*`, `CsTeams`/`CS_TEAM_*`, `InventorySlotType` and message argument types belong to specific APIs.
- Use named enums/macros for bit flags, slots, rounds, messages, damage, hulls and team values. Check if a selector is an ordinal or a bitmask before combining it with `|`. Leave enum values and macro expressions to the compiler.
- Read the selected ReAPI member's documented type and `Get params`/`Set params`: scalars, strings, vectors and indexed arrays have different variadic forms. `get_member`/`set_member` map to safe variants by default. Do not define `MEMBER_UNSAFE` as a routine optimization.

## Lifetime and context

- Validate the kind of target needed by the operation, not just a numeric range. World entity `0` can be valid for an engine operation and invalid for a player/member operation. Null/invalid entities can be `0`, `-1` or another declared sentinel depending on the API.
- Entity indices and client slots are reusable. For tasks, SQL, cvar queries or other delayed callbacks, retain and verify session identity (for example userid plus a generation) before applying results to a player. Authorization and put-in-server can arrive in either order.
- Distinguish owned handles from borrowed callback handles. Destroy owned arrays, tries, snapshots, iterators, stacks, datapacks, JSON, regex, parsers, files, SQL and traces with their matching API. A threaded SQL query handle is callback-owned and must not be freed by the plugin.
- Hook arguments, original returns, trace pointers, userinfo buffers and movement contexts are valid only in the context documented for that callback. Copy required data rather than retaining a borrowed pointer for deferred work.
- Keep gameplay hooks inexpensive. Cache cvar handles or bind values, cache message IDs, use event callbacks for discrete events, and perform disk/SQL/network work away from per-frame hooks. A task still runs on the game thread; moving blocking I/O into a task does not make it asynchronous.

## Validation

Compile with the target Pawn compiler and include set; resolve warnings about tags, deprecations and callback declarations. Exercise the changed behavior on the declared server stack when available, including the relevant disconnect/slot-reuse, world damage, bots, map changes or repeated config changes. Avoid claiming runtime compatibility solely from a successful compile.
