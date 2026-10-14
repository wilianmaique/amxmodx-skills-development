---
name: cs16-network-geoip
description: Implement AMXX nonblocking TCP/UDP socket state machines and GeoIP lookups for CS 1.6 plugins, including partial I/O, bounded polling, modern lookup variants and failure-aware client session handling.
---

# Sockets and GeoIP

Primary includes: `sockets.inc`, `geoip.inc`.

Read [shared contracts](../cs16-api-reference/references/shared-contracts.md). Retrieve exact flags, error codes and lookup signatures with [api_catalog.py](../cs16-api-reference/scripts/api_catalog.py), using the compiler's include set.

## Nonblocking networking

- Prefer `SOCK_NON_BLOCKING` for gameplay-triggered work and named `SOCK_LIBC_ERRORS` when the feature needs platform error detail. A numeric hostname avoids the documented blocking DNS lookup even when the socket itself is nonblocking.
- `socket_open` can return a still-connecting descriptor in nonblocking mode. Check writable readiness according to the native contract before sending; retain an explicit connect/send/read/complete/error state and deadline.
- Prefer `socket_is_readable` to deprecated `socket_change`. Timeouts are in microseconds and the default is a positive wait; use zero or a deliberately bounded value appropriate to the game thread. A repeating task does not make a blocking call asynchronous.
- Sends can be partial. Track a sent offset, queue the remaining bytes and read incrementally. Use `socket_send2` for payloads containing null bytes; `strlen` is not their length. TCP does not preserve application message boundaries.
- Inspect `socket_recv`'s bytes/termination capacity and distinguish peer close, no progress and actual errors as documented. Bound total payload, per-tick work and deadline to the requested protocol. Close owned descriptors on success, failure, disconnect cancellation and unload.

The provided sockets module is a TCP/UDP primitive, not a TLS/HTTP client. Do not claim an HTTPS request is protected by these includes alone. Use an existing appropriate module/service when the project already supplies the required protocol capability; do not introduce an insecure downgrade.

## GeoIP

Prefer `geoip_code2_ex`, `geoip_code3_ex` and `geoip_country_ex` over their deprecated predecessors. The old country-code APIs explicitly document an overflow on unknown lookup results. Use their fixed output dimensions and check the boolean/success result before displaying a country code.

Read city, region, timezone, latitude/longitude, continent and distance contracts individually. Some require a suitable installed GeoIP database and explicit language target. A failed lookup is not proof that a country or coordinate is zero/empty by design.

Choose the intended numeric IP form; do not assume every input includes or excludes a port in the same way. Avoid repeating lookups in per-frame hooks; cache at the relevant session/config lifetime and invalidate intentionally. GeoIP describes an IP-associated location, not verified player identity.

For delayed replies/lookup-driven state, revalidate the initiating client session before accessing slot data. Compile and check unknown IPs, loopback/private addresses, disconnected requesters and partial/failing I/O as relevant to the feature.
