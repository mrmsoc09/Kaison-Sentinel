# Production Runbook

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Startup
1) Ensure pgvector is running (if enabled)
2) Set required env:
   - `KAI_ENCRYPTION_KEY="..."` or `KAI_ALLOW_PLAINTEXT=1`
   - `KAI_ALLOW_NETWORK=1` (only if executing scans)
3) Start Kaison Sentinel API/UI
   - `python3 -m kai11.services.server --index ./outputs/vector_store.jsonl --host 127.0.0.1 --port 7878`
4) Optional async worker
   - `python3 -m kai11.worker`

## Rollback
- Revert container image to previous tag
- Restore `outputs/` from backup

## Backups
- Archive `outputs/` daily
- Snapshot pgvector volume weekly

## Program Scope Cache
- Refresh bug bounty program scopes:
  - `KAI_ALLOW_NETWORK=1 python3 scripts/fetch_program_guidelines.py --allow-network`
- Cache location: `data/programs/scopes/`
- Auto-sync (optional):
  - Enable in `config/options_override.json`:
    - `"program_sync": {"enabled": true, "auto_trigger": true, "interval_hours": 24}`
