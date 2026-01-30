# User Checklist (All Options)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Environment / CLI Options
- [ ] `KAI_ENCRYPTION_KEY` set (recommended) **or** `KAI_ALLOW_PLAINTEXT=1`
- [ ] `KAI_ALLOW_NETWORK=1` (allow network tools)
- [ ] `KAI_ALLOW_ACTIVE=1` (allow active scanning tools)
- [ ] `KAI_API_AUTH=1` (enable API key auth)
- [ ] `KAI_VECTOR_BACKEND=pgvector` (pgvector backend)
- [ ] `KAI_RUN_DB=pg` (store run metadata in Postgres)
- [ ] Enable auto program sync in `config/options_override.json` (program_sync)

## UI — Guided Plan
- [ ] Goal
- [ ] Targets (allowlist)
- [ ] Constraints
- [ ] Playbook IDs (comma-separated)
- [ ] MITRE Technique ID
- [ ] Module Kind: OSINT / Vuln / All
- [ ] Role: Analyst / Operator / Admin
- [ ] Report Format (template selector)

## UI — Execution
- [ ] Approve (HiL)
- [ ] Validation Confirmed (HiL)
- [ ] Report HiL Confirmed
- [ ] Mitigation Tier: Minimal / Standard / Deep

## UI — MITRE Planner
- [ ] Technique selection
- [ ] Allowlist
- [ ] HiL approval
- [ ] Generate MITRE Plan
- [ ] Export MITRE Report Bundle
- [ ] Auto-fill playbooks + technique into plan

## UI — API Access
- [ ] X-API-Key (local storage)

## UI — Setup Hub
- [ ] Mark setup steps complete/in progress
- [ ] Program scopes cache sync (Sync now)

## UI — Proxy Overrides
- [ ] HTTP proxy
- [ ] HTTPS proxy
- [ ] NO_PROXY list

## UI — Vault / API Keys
- [ ] Source ID
- [ ] API key value
- [ ] Add key

## UI — Outputs / Diagnostics
- [ ] Traces
- [ ] LangStudio evals
- [ ] BigQuery exports
- [ ] Loop state + audit

## UI — Playbooks
- [ ] Create playbook (id/name/modules)
- [ ] Import JSON/CSV
- [ ] Export playbooks

## UI — Stakeholder Email
- [ ] Profile name / org / email
- [ ] Provider (Gmail SMTP / Proton Bridge / Custom SMTP)
- [ ] SMTP host/user/port
- [ ] Password source (vault id)
- [ ] STARTTLS / SSL
- [ ] Enable send
- [ ] Draft email
- [ ] Queue email (HiL confirmed)

## UI — Evidence
- [ ] run_id
- [ ] finding_id
- [ ] evidence kind (screenshot/pcap)
- [ ] file path
- [ ] attach

## UI — Export Bundle
- [ ] run_id → Generate bundle

## Core Config Files (editable options)
- [ ] `config/options_master.json` (global options)
- [ ] `config/options_override.json` (runtime overrides)
- [ ] `config/programs.json` (program list + scope URLs)
- [ ] `config/policy.json` + `config/policy_rules.json` (RBAC/deny rules)
- [ ] `config/tools_osint.json` / `config/tools_vuln.json` (tool configs)
- [ ] `config/tool_registry.json` / `config/tool_substitutes.json`
- [ ] `config/playbooks/*.json` (playbook definitions)
- [ ] `config/mitre_attack.json` (MITRE technique catalog)
- [ ] `config/mitre_report_formats/*` (MITRE report templates)
- [ ] `config/report_formats/*` (report templates)
- [ ] `config/intelligence_lifecycle.json` (intel labeling)
- [ ] `config/webhooks.json` (webhooks)
- [ ] `config/retention.json` (retention)
