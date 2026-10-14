---
name: cs16-data-containers
description: Choose and manage AMXX dynamic arrays, trie maps/iterators/snapshots, stacks, datapacks and sorting for CS 1.6 plugin state with correct block sizes, mutation rules, callback types and handle lifetime.
---

# AMXX data containers

Primary includes: `cellarray.inc`, `celltrie.inc`, `cellstack.inc`, `datapack.inc`, `sorting.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Query each creation/access/destruction or sorting callback contract with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py).

## Choose the representation

- Fixed per-client state: use a fixed array with a session/reset policy when the key really is a bounded player slot.
- Ordered or indexed dynamic records: `Array:`; choose `cellsize` to fit one entire element. Reserved capacity is not the number of valid elements. Use push/resize operations before indexed access.
- String-key lookup: `Trie:`. Read getter boolean results before using output values; missing keys differ from a stored zero or empty string. Preserve `replace` policy when setting keys.
- LIFO work: `Stack:` with a suitable block size. Pop functions report whether an element was available; empty is not an arbitrary zero value.
- Heterogeneous transferable payload: `DataPack:`. Read fields in the same order/type as written and reset its position deliberately. A handle does not validate session identity on its own.

Read [ownership and iteration](references/ownership-and-iteration.md) for iterator/snapshot lifetime and opaque datapack positions.

## Efficient lookup and sorting

Prefer `TrieIterCreate` for cheap short-lived read-only iteration when keys will not be added/deleted. Such key mutations invalidate iterators; replacing an existing value is allowed. Use a key snapshot or staged mutation if the algorithm needs structural changes during traversal, and destroy the snapshot/iterator independently.

For arrays, prefer `ArraySortEx` when direct-element comparisons suit the record shape. Its callback receives scalar elements for cellsize 1 and array elements for larger cellsize. `ArraySort` passes item indices; translating its callback unchanged is incorrect.

Use `SortIntegers`, `SortFloats`, `SortStrings` or `SortADTArray` for their matching type and `SortMethod`/`SortType`. Custom comparisons return negative/zero/positive according to the documented order. Avoid comparator subtraction that can overflow, and do not mutate the container from inside its comparator.

## Handle correctness

Pair each owned container with its destroy native and invalidate retained aliases according to that API. Copying a handle is not cloning its contents. `ArrayClone` is the explicit array clone operation; storing other handles inside a container does not transfer their ownership or destroy them automatically.

Read array string/access size semantics before copying. Do not use the `DoNotUse:ArrayGetStringHandle` shortcut for new code or retain an internal string pointer across mutations. Maintain explicit bounds after insertion/deletion because item indices shift.

Compile and check empty containers, missing keys, capacity versus element count, iterator mutation and cleanup. Choose verification cases based on the actual data algorithm rather than asserting wording or wrapper implementation.
