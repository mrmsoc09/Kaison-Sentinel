# Kaison Sentinel

![Status](https://img.shields.io/badge/status-mvp-ready?style=flat-square&color=gold)
![Mode](https://img.shields.io/badge/mode-offline--first?style=flat-square&color=orange)
![Governance](https://img.shields.io/badge/governance-HiL%20gated?style=flat-square&color=blue)

This repository contains the Kaison Sentinel offline-first build for:
- ingesting local files from `/home/user23/KAI`
- generating self-supervised training data
- creating a local vector database using hashed embeddings (pure Python)

No network calls are made. The vector store and training data are written under `outputs/`.

## Quick start

1) Build vector DB + training data
```
python3 -m kai11.pipelines.pipeline --source . --out ./outputs
```

2) Run the local search server (optional)
```
python3 -m kai11.services.server --index ./outputs/vector_store.jsonl
```

## Full stack (pgvector)
```
docker compose -f docker-compose.full.yml up --build
```

Environment variables:
- `KAI_VECTOR_BACKEND=pgvector`
- `KAI_PGVECTOR_DSN` (optional; overrides host/user/pass vars)
- `KAI_RUN_DB=pg` (optional; store run metadata in Postgres)

## API auth (optional)
Enable header‑based auth:
```
export KAI_API_AUTH=1
```
Default header is `X-API-Key` configured in `config/api_auth.json`.
Rate limiting is enabled by default via `config/api_limits.json`.

## API docs
See `docs/API.md`.

## Async worker
```
python3 -m kai11.worker
```

## Webhooks / Retention
See `docs/WEBHOOKS.md` and `docs/RETENTION.md`.

## Kubernetes (minimal)
```
kubectl apply -f k8s/pgvector.yaml
kubectl apply -f k8s/kaison-deployment.yaml
```

3) Generate a scan plan (scope required)
```
python3 -m kai11.cli --mode plan --scope '{"allowlist":["example.com"]}'
```

4) Execute (HiL approval required)
```
# encryption is required unless KAI_ALLOW_PLAINTEXT=1
export KAI_ENCRYPTION_KEY="replace-with-strong-key"
python3 -m kai11.cli --mode execute --scope '{"allowlist":["example.com"],"validation_confirmed":true,"report_hil_confirmed":true}' --approve --tier standard
```

## OSINT core tools (install)
```
bash scripts/install_osint_core.sh
```

## Vulnerability core tools (install)
```
bash scripts/install_vuln_core.sh
```

## Smoke test (offline)
```
python3 scripts/smoke_test_osint.py
python3 scripts/smoke_test_vuln.py
```

## Outputs
- `outputs/vector_store.jsonl` (vector DB, JSONL)
- `outputs/training_data.jsonl` (self-supervised training pairs)
- `outputs/stats.json` (ingest/index stats)
- `outputs/runs/` (run records; encrypted if key set)
- `outputs/reports/` (reports; encrypted if key set)
- `outputs/logs/` (audit logs)
- `outputs/alerts/` (local alert payloads)
- `outputs/bigquery/` (offline BigQuery JSONL exports)
- `outputs/loops/` (loop state snapshots for GUI)
- `outputs/traces/` (LangStudio traces)
- `outputs/langstudio/` (LangStudio evals)

## Structure
See `docs/TREE.md` for the full file tree after the refactor.

## Governance (OSINT/Recon)
- Rules and lifecycle labels live in `PRAISON.md`, `.praison/rules/`, and `config/intelligence_lifecycle.json`.
- Intelligence is never deleted; it is labeled (raw/candidate/actionable/validated/contextual) to control routing.

## MITRE Planner (defensive)
- `GET /api/mitre/techniques` to list supported techniques.
- `POST /api/mitre/plan` to generate HiL-gated, read-only assessment plans.
- `POST /api/mitre/export` to generate a MITRE plan report bundle.

## Optional Scale Paths (planned)
- **DeepAgents** (LangChain) for long-horizon investigations and attacker-style chaining.
- **Haystack** pipelines for advanced RAG, validation loops, and retrieval evaluation.
- **n8n** for scheduling, approvals, and external integrations (ticketing/notifications).
- **LangGraph/LangSmith** for durable workflows and observability in later phases.
