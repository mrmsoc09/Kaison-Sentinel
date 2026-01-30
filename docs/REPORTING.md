# Reporting Module

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

Reports can be generated in Markdown/HTML/JSON/CSV/PDF/SARIF using templates under `config/report_formats/`.
MITRE plan reports use `config/mitre_report_formats/`.

## Selection
Use `report_format_id` in scope or choose in UI.

## Validation
For vuln runs, reports are blocked until `validation_confirmed: true`.

## Context fields (auto-populated)
- MITRE context (`mitre_technique_id`)
- Playbook context (`playbook_ids`)
- Validation recommendation (based on severity distribution)
