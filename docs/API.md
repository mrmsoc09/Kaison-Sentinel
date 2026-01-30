# API Reference (Local)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

All endpoints are local-only by default. If API auth is enabled, include `X-API-Key`.

## Auth
- Header: `X-API-Key`
- Enable: `export KAI_API_AUTH=1`

## Core
- `GET /api/assets/*` — registry and assets
- `GET /api/options` — merged options
- `GET /api/options?kind=osint|vuln|validation` — per-module options
- `POST /api/options/override` — set runtime overrides
- `GET /api/setup/hub` — setup steps
- `POST /api/setup/hub` — update setup step
- `GET /api/mitre/techniques` — list MITRE planner techniques
- `POST /api/mitre/plan` — generate MITRE plan
- `POST /api/mitre/export` — generate MITRE plan + report bundle

## Execution
- `POST /api/plan` — generate plan
- `POST /api/execute` — execute with HiL approval
- `POST /api/execute/async` — enqueue async execution
- `GET /api/jobs` — job queue status

### Plan/Execute Scope Fields
- `playbook_ids` — optional list of playbook ids (filters modules)
- `mitre_technique_id` — optional MITRE technique id for report context

## Vault
- `GET /api/vault/providers`
- `GET /api/vault/keys`
- `POST /api/vault/add`

## Evidence & Reports
- `POST /api/evidence/attach`
- `GET /api/exports/bundle?run_id=...`

## Email
- `POST /api/email/draft`
- `POST /api/notify/email`
- `GET /api/email/config`
- `POST /api/email/config`

## Outputs
- `GET /api/outputs/traces`
- `GET /api/outputs/evals`
- `GET /api/outputs/bigquery`
- `GET /api/outputs/loops`
- `GET /api/loops/state`
