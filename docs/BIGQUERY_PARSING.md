# BigQuery Parsing (Offline Export)

Kaison Sentinel generates BigQuery-ready JSONL exports for:
- artifacts
- findings
- evidence
- traces
- reports
- training

Exports are written to `outputs/bigquery/` per run. Loading to BigQuery is disabled by default
and only occurs if `config/bigquery.json` has `enabled: true` and valid credentials.
