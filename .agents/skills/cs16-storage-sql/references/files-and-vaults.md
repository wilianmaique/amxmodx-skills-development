# Files and vaults

## Path and stream contracts

AMXX file natives can use host filesystem access or Valve filesystem access, with `use_valve_fs` and path IDs on selected functions. Those options are not present on every native, and their defaults differ. Inspect the exact declaration before mixing handles or interpreting a relative path.

`fopen` returns an owned file handle and `fclose` releases it. Directory handles from `open_dir` use `next_file` and `close_dir`, not `fclose`. Distinguish EOF from successfully reading a complete logical record; inspect return values and truncation behavior for long lines.

Raw `fread*`/`fwrite*` modes and typed `FileRead*`/`FileWrite*` functions encode different widths/counts. `fread_raw` has blocksize and blocks; `fwrite_raw` has its own parameter order. Preserve the exact byte format for an existing file. `fseek` uses an origin constant; a byte position does not become a container index.

For replacing valuable existing data, use a complete checked write before replacing the old file if the project's format/lifetime needs that protection. Do not invent atomicity guarantees for a rename across filesystem backends. Keep any schema/version marker part of the established format or an intentional migration.

## nVault data

`nvault_get` is overloaded for integer, Float and string outputs; inspect the selected form. `nvault_lookup` returns existence explicitly and writes the timestamp. `nvault_set` timestamps a record, while `nvault_pset` makes a permanent record according to its documented pruning behavior.

All nVault timestamps are UNIX epoch values. Use `get_systime`-compatible values for `nvault_touch`/`nvault_prune`, not map `get_gametime`. Check the start/end boundary and permanent-record behavior before pruning. Do not prune unrelated plugin data in a shared vault.

Choose a persistent account key after authorization. A slot index or nickname is not a stable account identity. Decide how bots, pending IDs and unsupported authentication types are handled without corrupting another user's record.

For legacy global-vault migration, read the old key/value format first. Convert only the requested plugin's records, retain an intentional recovery path and avoid deleting source data merely because the new module loads. Neither a different vault native nor a new filename migrates the contents automatically.
