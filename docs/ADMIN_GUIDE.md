# Admin Guide

## Core switches
- `KAI_ALLOW_NETWORK=1` to allow network tools.
- `KAI_ALLOW_ACTIVE=1` to allow active scanning tools.
- `KAI_API_AUTH=1` to enforce API key auth.
- `KAI_VECTOR_BACKEND=pgvector` to use pgvector.
- `KAI_RUN_DB=pg` to store run metadata in Postgres.

## Secrets
Use the vault (`/api/vault/add`) and encryption key via `KAI_ENCRYPTION_KEY`.

## Policy
Adjust `config/policy.json` and `config/options_master.json` for allowed techniques.
