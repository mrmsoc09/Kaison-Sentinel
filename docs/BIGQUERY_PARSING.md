# BigQuery Parsing (Offline Export)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

Kaison Sentinel generates BigQuery-ready JSONL exports for:
- artifacts
- findings
- evidence
- traces
- reports
- training

Exports are written to `outputs/bigquery/` per run. Loading to BigQuery is disabled by default
and only occurs if `config/bigquery.json` has `enabled: true` and valid credentials.
