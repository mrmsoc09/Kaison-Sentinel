# Start Here (10-minute path)

1) Build the local vector DB
```
python3 -m kai11.pipelines.pipeline --source . --out ./outputs
```

2) Generate a scan plan (no execution)
```
python3 -m kai11.cli --mode plan --kind osint --role operator --scope '{"allowlist":["example.com"]}'
```

3) Review outputs
- `outputs/` for logs, evidence, and reports
- `outputs/tool_health.json` for installed tool status

4) Launch local UI
```
python3 -m kai11.services.server --index ./outputs/vector_store.jsonl --host 127.0.0.1 --port 7878
```

5) Optional: execute (requires approval + allow network)
```
export KAI_ALLOW_NETWORK=1
export KAI_ALLOW_ACTIVE=1
python3 -m kai11.cli --mode execute --kind osint --role operator --approve --scope '{"allowlist":["example.com"]}'
```
