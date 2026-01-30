# Execution Notes

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

- Execution is disabled by default. To enable networked checks:
  - set `KAI_ALLOW_NETWORK=1`
- Active tools require:
  - set `KAI_ALLOW_ACTIVE=1`
- Encrypted storage is required unless explicitly disabled:
  - set `KAI_ENCRYPTION_KEY="..."` or `KAI_ALLOW_PLAINTEXT=1`

Optional scope fields:
- `playbook_ids`: list of playbook ids to constrain modules
- `mitre_technique_id`: includes MITRE context in reports

Default modules are safe-mode by default unless network is enabled.
