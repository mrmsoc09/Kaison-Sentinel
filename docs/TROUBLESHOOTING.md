# Troubleshooting

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## UI not loading
- Ensure server is running: `python3 -m kai11.services.server --index ./outputs/vector_store.jsonl`
- If port is blocked, set `--port 7878` and use `http://localhost:7878`

## Reports blocked
- Validate HiL confirmation and evidence (screen recording required).
- Ensure `KAI_ENCRYPTION_KEY` or `KAI_ALLOW_PLAINTEXT=1` is set.

## API returns 401
- If `KAI_API_AUTH=1`, set `X-API-Key` in the UI.

## pgvector errors
- Ensure `docker-compose.full.yml` is running and `psycopg` is installed.

## Network tools not running
- Set `KAI_ALLOW_NETWORK=1` and `KAI_ALLOW_ACTIVE=1` if required by the module.

## Tool missing
- Install with `scripts/install_osint_core.sh` or `scripts/install_vuln_core.sh`.
