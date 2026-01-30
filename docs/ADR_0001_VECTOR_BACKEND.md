# ADR 0001 — Vector Backend

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

**Decision:** Support file‑based sparse vector store with optional pgvector backend.  
**Reasoning:** Offline default, deterministic hashing; pgvector offers scalable search when available.  
**Status:** Accepted.
