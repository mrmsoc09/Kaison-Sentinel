# Troubleshooting

## UI not loading
- Ensure server is running: `python3 -m kai11.services.server --index ./outputs/vector_store.jsonl`

## Reports blocked
- Validate HiL confirmation and evidence (screen recording required).

## API returns 401
- If `KAI_API_AUTH=1`, set `X-API-Key` in the UI.

## pgvector errors
- Ensure `docker-compose.full.yml` is running and `psycopg` is installed.
