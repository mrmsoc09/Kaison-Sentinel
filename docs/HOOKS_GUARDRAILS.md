# Hooks & Guardrails

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Hooks
Configured in `config/hooks.json` and enforced in `core/hooks.py` + `core/tool_exec.py`.

- Pre-hook: block empty targets
- Post-hook: attach evidence metadata (tool_id, target, timestamp)

## Guardrails
Implemented in `core/guardrails.py` and applied in `core/scan_engine.py`.

- No deletions: labels are downgraded when evidence/HiL is missing
- Actionable/validated are labels only (do not filter data)

