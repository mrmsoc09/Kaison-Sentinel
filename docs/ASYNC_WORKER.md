# Async Worker

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

Start the worker to process queued jobs:
```
python3 -m kai11.worker
```

Enqueue async execution:
```
POST /api/execute/async
```
