# MITRE Planner (Defensive, Read‑Only)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

The MITRE planner produces **HiL‑gated, read‑only assessment plans** indexed by MITRE tactic/technique.
It does **not** perform exploitation, evasion, or destructive behavior.

## What it Does
- Maps techniques to safe objectives
- Enforces scope + HiL gates
- Recommends module playbooks (OSINT / Vuln / Validation)
- Generates MITRE plan report bundles (md/html/json/csv/pdf)

## UI behavior
- MITRE Planner can auto‑fill playbook IDs and technique id into the Guided Plan.

## Configuration
- `config/mitre_attack.json` — technique catalog
- `config/mitre_report_formats/` — report templates

## API
- `GET /api/mitre/techniques`
- `POST /api/mitre/plan`
- `POST /api/mitre/export`

## Safe Extension Guidelines
- Use **read‑only** steps only.
- Keep HiL + scope gates enabled.
- Add validation playbooks for evidence collection.
