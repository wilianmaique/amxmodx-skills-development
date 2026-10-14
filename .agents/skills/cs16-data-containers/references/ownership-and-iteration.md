# Ownership and iteration

| Owned object | Matching destruction |
| --- | --- |
| `Array:` from `ArrayCreate`/`ArrayClone` | `ArrayDestroy` |
| `Trie:` | `TrieDestroy` |
| `Snapshot:` from `TrieSnapshotCreate` | `TrieSnapshotDestroy` |
| `TrieIter:` from `TrieIterCreate` | `TrieIterDestroy` |
| `Stack:` | `DestroyStack` |
| `DataPack:` | `DestroyDataPack` |

Inspect whether the destruction native takes the handle by reference and invalidates the caller's variable. Other copies of the same cell can remain stale aliases; do not destroy them a second time. A container of handles still needs a deliberate ownership policy for each child.

## Arrays and stacks

`ArrayCreate(cellsize, reserved)` allocates capacity; a newly created array has no valid indexed elements just because `reserved` is positive. `cellsize` is cells per record. For string records, allow the full string storage and terminator in the block; inspect the selected `ArrayGetString` size contract instead of assuming every length is interchangeable with `charsmax`.

Array insertions/removals shift later indices. Traverse backwards when deleting by index, or collect indices and apply a controlled mutation. Reads/writes of an array element with a custom enum record must fit the entire block. `ArraySetCell`'s block/character mode is different from replacing the full record.

Stacks also have a block size; popping into an undersized array/string is not made safe by the number of stack elements. Check the pop result, preserve written-length output where needed, and distinguish clearing from destroying.

## Trie traversal

Adding/removing keys invalidates active iterators. Replacing the value under an existing key is allowed and visible to iteration. Iterators are inexpensive and short-lived; do not keep them for a later task while the map can change.

Snapshots expose a captured list of keys, not a snapshot clone of every value. If a key can be removed after snapshot creation, a subsequent trie getter can fail. Keys are not promised to be sorted. Use `TrieSnapshotKeyBufferSize` or an appropriate maintained key bound before retrieving keys.

## Datapacks

`ResetPack(pack, false)` resets position without discarding contents; `true` clears them. Match `WritePackCell`/`WritePackFloat`/`WritePackString` to reads in the same sequence. `GetPackPosition` returns an opaque `DataPackPos:` usable only through `SetPackPosition`; never compute an offset by adding an assumed number of cells or bytes.

`IsPackEnded` can stop traversal but does not reveal the next value's type. Store a schema/type discriminator if the payload format is variable. The plugin must free every datapack it owns, including cancelled/deferred-operation paths; task cancellation itself does not free a handle contained in that task's payload.
