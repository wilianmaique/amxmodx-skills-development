# SQL ownership and asynchronous sessions

## Handle ownership

| Resource | Ownership |
| --- | --- |
| `SQL_MakeDbTuple` / `SQL_MakeStdTuple` result | Plugin-owned tuple; free when no longer needed |
| `SQL_Connect` result | Plugin-owned synchronous connection; free after dependent queries |
| `SQL_PrepareQuery` result | Plugin-owned synchronous query; free after use |
| `SQL_ThreadQuery` callback `query` | Borrowed callback handle; do not free |

The tuple is connection information, not an open database connection. `SQL_ThreadQuery` prepares/executes asynchronously and the documented implementation connects/disconnects per query. Do not pass a tuple to a native that requires a live database handle simply because both use `Handle:`.

## Query callback

Use the exact public callback:

```pawn
public QueryHandler(failstate, Handle:query, error[], errnum,
    data[], size, Float:queuetime)
```

Check `TQUERY_*` first. On success, distinguish zero rows from a present row and check null columns before interpreting typed output. Read a row, then advance with the correct `SQL_NextRow`/result API. Column indices come from SQLX's declared contract; DBI's field numbering is not the same API.

Carry a bounded copied payload such as player id, userid and request generation. Validate payload size before access and the current session before applying player results. A newer request can supersede an older request in the same session; add a per-feature request token when order matters.

For disconnect saves, capture the persistent key and record values before the player entity is removed. Completion can be logged or handled without assuming the same client slot remains occupied. Do not send a completion message to a departing client from the disconnect forward.

## SQL text and driver behavior

`SQL_PrepareQuery` and formatted helpers construct SQL text; they do not document prepared-statement parameter binding. Quote data through `SQL_QuoteString`/`SQL_QuoteStringFmt`. The supplied quote native accepts a live database handle for localization or `Empty_Handle` if no connection is available; read the chosen driver/charset behavior before using the latter for an external database. A tuple is not a valid quoting connection.

Allocate enough output for worst-case expansion (the include notes twice the input length, plus storage for termination), use the native's maximum-length convention and handle `-1`. Keep source and output buffers separate as documented. Quoting values does not validate table/column names; choose those from known identifiers.

`SQL_SetCharset` can apply to handles according to its declared behavior; configure the connection/tuple at the correct phase for the selected mode. `SQL_SetAffinity` changes driver selection semantics and is not a per-query namespace. Preserve the project's MySQL/SQLite choice and schema rather than translating syntax by guesswork.

Keep credentials in the existing configuration mechanism. A useful error report contains the operation and driver error, with sensitive connection data omitted.
