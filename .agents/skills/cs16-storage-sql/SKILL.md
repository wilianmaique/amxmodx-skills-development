---
name: cs16-storage-sql
description: Implement AMXX file, nVault and SQLX persistence for CS 1.6 plugins, including threaded SQL session validation, resource ownership and deliberate migration from global vault or DBI storage.
---

# Files, nVault and SQLX

Primary includes: `file.inc`, `nvault.inc`, `vault.inc`, `sqlx.inc`, `dbi.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md) and query exact API contracts with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py). Select storage by the data model and existing saved format; adding ReAPI is unnecessary for persistence alone.

## Files and local key/value data

- Use maintained AMXX data/config directory helpers and the native's filesystem/path-id contract. Do not hardcode the development machine's absolute paths into a server plugin.
- Prefer stream reads with `fopen`/`fgets`/`fclose` for sequential files; repeated `read_file` line lookups are appropriate only when their specific contract fits. Check open/read/write outcomes and close owned file/directory handles on all paths.
- Text, raw blocks and typed integer reads/writes use different modes and counts. Read `BLOCK_*`, seek origin, `FileType`, permission and time constants before using them. A size in cells is not automatically a byte count.
- Use nVault for simple named persistent keys. `nvault_open` fails with `INVALID_HANDLE` (`-1`); a valid integer handle is not a generic AMXX tagged handle. Close it at plugin shutdown.
- Use `nvault_lookup` when existence and timestamp matter; a numeric zero from an overloaded get does not establish that a key is absent. Choose timestamped versus permanent writes deliberately and use epoch times for touch/prune.
- Keep `vault.inc` for a deliberate existing global-vault compatibility path. New nVault storage should not silently overwrite or reinterpret the old vault's records.

Read [files and vaults](references/files-and-vaults.md) for timestamp and data migration details.

## SQLX

Prefer SQLX to the older DBI interface for new SQL work. Use `SQL_ThreadQuery` for gameplay-driven queries so connection/query delays do not block the game loop. Read [SQL ownership and sessions](references/sql-ownership-and-sessions.md) before implementing a callback.

- Distinguish a database tuple, connection, prepared query and callback-owned query even though SQLX uses `Handle:` for all of them.
- The threaded callback is `(failstate, Handle:query, error[], errnum, data[], size, Float:queuetime)`. Check `TQUERY_*` failure states before reading rows. Do not free its query handle.
- Pass a copied payload identifying the requesting player session. Revalidate userid/generation on completion before modifying a connected slot. A task around a synchronous query does not make it asynchronous.
- SQLX prepared-query formatting is not automatic SQL parameter binding. Quote untrusted string values with the documented quote API and length contract; allowlist identifiers separately. Handle quote failure and preserve the selected charset/driver semantics.
- Initialize tuples after connection settings have executed. Never write credentials into logs or generated examples. Free owned tuples, synchronous connections and queries with their matching lifetime.
- Read `SQL_MoreResults`, `SQL_NextRow`, result indices, null values, affected-row/insert-ID and multi-result semantics before iteration. Empty successful results differ from a failed query.

## Migration and validation

DBI column/result conventions differ from SQLX; rewriting function names alone is incorrect. Preserve saved keys, schemas, driver, rank/account identity and error behavior. Keep a data conversion separate and reviewable when one is required.

Compile against the chosen module includes. Verify malformed/missing files, empty values, open failure, SQL failure/no rows and disconnect/slot reuse during a query as relevant to the change. State when database/live-server behavior has not been exercised.
