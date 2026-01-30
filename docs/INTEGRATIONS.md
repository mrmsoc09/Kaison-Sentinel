# Integrations

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## BigQuery
- Config: `config/bigquery.json`
- Loader: `kai11/integrations/bigquery_loader.py`
- Parsing/export: `kai11/core/bigquery_export.py`
- Status: implemented (disabled by default)

## Vertex AI (Google DL)
- Config: `config/vertex_ai.json`
- Client: `kai11/integrations/vertex_ai_client.py`
- Status: implemented (disabled by default; requires pipeline spec URI)

## Dependencies (when enabled)
- google-cloud-bigquery
- google-cloud-aiplatform
- google-auth

## Planned Integrations (optional)
- DeepAgents (LangChain): long-horizon OSINT investigation and chaining.
- Haystack: retrieval pipelines and evaluation loops.
- n8n: external workflow automation (approvals, notifications).
