---
name: cs16-math-time
description: Implement AMXX Float arithmetic, vectors, XS geometry and time formatting/deadlines for CS 1.6 plugins with correct tags, units, angle conventions and gameplay versus realtime versus epoch clocks.
---

# Math, geometry and time

Primary includes: `float.inc`, `vector.inc`, `xs.inc`, `time.inc`. Clock natives are also declared in `amxmodx.inc` and ReAPI engine headers.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Query the actual native/stock and any conditional XS macro using [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py); use `--implementation` for behavior-sensitive stocks and `raw` for active macro conditions.

## Numeric representation

Use `Float:` values for game origins, velocities, angles and floating-point intervals. Convert integer numbers with `float()` and convert back with `floatround()` using the required rounding mode. A `Float:` tag cast reinterprets bits; it is not numeric conversion.

Read the selected trig native's `anglemode` contract and pass degrees/radians explicitly when required. `floatatan2`'s declared argument order must be followed rather than importing another language's convention. XS provides conditional compatibility wrappers/macros; these are not automatically a better choice than current Float natives.

The supplied `xs_atan2` macro expands to a two-argument `floatatan2` call, while this `float.inc` declares an explicit radix argument. Prefer the direct verified native call with its mode and compile it; do not copy an unverified wrapper simply because it exists in a stock include.

## Vectors and geometry

Use the actual vector representation: integer origin arrays belong to integer-distance/conversion APIs; engine movement and `var_*` vectors are Float arrays. `IVecFVec`/`FVecIVec` explicitly convert representations with their own rounding behavior.

Use native vector helpers or the specific `xs_vec_*`/plane/projection helpers appropriate to the math. Preserve axis/angle conventions and output shape. Read whether output may alias an input before doing in-place operations. Guard zero-length/degenerate geometry when normalizing, dividing, finding an angle or intersecting a plane.

For frequent radius comparisons, squared distance can avoid a square root when the threshold is squared in the same units. Do not replace a true distance result with its square if the value is later displayed or used as a linear quantity.

## Time domains

- `get_gametime`: map/game time for gameplay deadlines; resets with the map and has game-time semantics.
- ReHLDS `rh_get_realtime`: engine realtime for a feature that explicitly needs that clock and capability.
- `get_systime`: UNIX epoch for persisted timestamps, nVault pruning and real-world expiry.
- `time.inc` `get_time_length` and unit constants: duration formatting, with the documented unit/count and language target.

Never compare persisted epoch timestamps to map time. Do not assume a task is a wall-clock alarm or a frame delta. Choose what should happen across pause, map change and restart before selecting the clock.

XS also includes string, logging and task-payload helpers. Prefer the dedicated modern string/task APIs where they satisfy the feature, and inspect XS's implementation/state when an existing plugin relies on its specialized helpers. Do not use its shared internal task buffers as an unexplained concurrent storage mechanism.

Compile and check the relevant mathematical boundaries, rounding, units and reset/expiry behavior. Use meaningful cases rather than testing every elementary Float operation.
