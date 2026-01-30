# Admin Guide

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Core switches
- `KAI_ALLOW_NETWORK=1` to allow network tools.
- `KAI_ALLOW_ACTIVE=1` to allow active scanning tools.
- `KAI_API_AUTH=1` to enforce API key auth.
- `KAI_VECTOR_BACKEND=pgvector` to use pgvector.
- `KAI_RUN_DB=pg` to store run metadata in Postgres.
- `KAI_ALLOW_PLAINTEXT=1` to store reports without encryption (local/dev only).

## Secrets
Use the vault (`/api/vault/add`) and encryption key via `KAI_ENCRYPTION_KEY`.
Reports require encryption unless `KAI_ALLOW_PLAINTEXT=1`.

## Policy
Adjust `config/policy.json` and `config/options_master.json` for allowed techniques.
