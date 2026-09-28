# MVCC Snapshot Isolation Engine Skill

Robust, zero-dependency Python implementation of **Multi-Version Concurrency Control (MVCC)** supporting non-blocking concurrent reads and writes with periodic epoch vacuuming.

## Features
- **Temporal Version Visibility**: Every record maintains `created_ts` and `expired_ts` intervals.
- **Lock-Free Reads**: Concurrent reads never block concurrent writes; reads observe pure immutable point-in-time snapshots.
- **Epoch Garbage Collection**: Vacuuming cleans obsolete record versions safely below active transaction watermarks.
- **Zero External Dependencies**: Pure Python standard library.
- **Native MCP Protocol**: JSON-RPC 2.0 stdio server compatible with Claude Desktop, Cursor, and Windsurf.

## Architecture
```mermaid
graph TD
    ClientRead["Read Snapshot at ts=25"] --> VList["Version List for Key 'balance'"]
    VList --> V1["Version 1: [10, 20) -> 1000"]
    VList --> V2["Version 2: [20, 30) -> 1250 (MATCHED)"]
    VList --> V3["Version 3: [30, inf) -> 800"]
```
