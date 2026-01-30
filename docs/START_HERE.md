# Start Here (10-minute path)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

Prereqs: Python 3, local repo, and either `KAI_ENCRYPTION_KEY` or `KAI_ALLOW_PLAINTEXT=1`.
See `docs/USER_CHECKLIST.md` for all configurable options.

1) Build the local vector DB
```
python3 -m kai11.pipelines.pipeline --source . --out ./outputs
```

2) (Optional) Generate a MITRE plan + auto-fill playbooks
```
python3 -m kai11.cli --mode plan --kind all --role operator --scope '{"allowlist":["example.com"],"mitre_technique_id":"T1562.001","playbook_ids":["playbook.osint.basic","playbook.vuln.basic","playbook.vuln.validation"]}'
```

3) Generate a scan plan (no execution)
```
python3 -m kai11.cli --mode plan --kind osint --role operator --scope '{"allowlist":["example.com"]}'
```

4) Review outputs
- `outputs/` for logs, evidence, and reports
- `outputs/tool_health.json` for installed tool status

5) (Optional) Refresh public program scope cache
```
python3 scripts/fetch_program_guidelines.py
```

6) Launch local UI
```
python3 -m kai11.services.server --index ./outputs/vector_store.jsonl --host 127.0.0.1 --port 7878
```

7) Optional: execute (requires HiL approval + allow network)
```
export KAI_ALLOW_NETWORK=1
export KAI_ALLOW_ACTIVE=1
export KAI_ENCRYPTION_KEY="your-strong-key"  # or KAI_ALLOW_PLAINTEXT=1
python3 -m kai11.cli --mode execute --kind osint --role operator --approve --scope '{"allowlist":["example.com"]}'
```
