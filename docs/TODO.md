# TODO (Status)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Completed
- System contract and schemas (core contracts, mitigation schema, scope model)
- Governance + approvals (scope enforced, HiL gates, safe-mode flags)
- Module framework (registry + 1Tool/1Agent/1Job wrappers)
- Evidence + audit (evidence bundles, audit log, redaction)
- OSINT/Recon pipeline structure (163 tools, playbooks, circle orchestration)
- Vulnerability module pipeline (separate circle + toolchain)
- Mitigation engine (tiered output, dry‑run/apply/verify/rollback)
- Orchestration scaffolding (circle + LangStudio config + PraisonAI config)
- Full LangChain/LangGraph/LangSmith flow customization per module (config-driven)
- Inter‑tool communication bus
- Storage layer (run records + reports, encryption support)
- Encryption key management/rotation policies
- Reporting (basic report generator)
- Test + validation suite (policy, redaction, evidence)
- UI/UX implementation (dashboard, findings board, evidence locker)
- Enterprise guardrails (RBAC, policy‑as‑code)
- File tree restructure + documentation
- BigQuery loader implementation (google-cloud-bigquery)
- Vertex AI integration implementation (google-cloud-aiplatform)
- Tool‑specific command tuning and parsers (baseline configs applied)
- PraisonAI OSINT governance + lifecycle labels (retain all data)
- PraisonAI OSINT workflows (YAML) and hooks/guardrails
- LangStudio offline adapters (tracing, evals, LangGraph runner)
- DeepAgents offline planner with optional runtime adapter
- BigQuery parsing/export (offline JSONL)
- MITRE ATT&CK defensive planner (HiL-gated, read-only)

## In Progress
- None

## Pending
- None
