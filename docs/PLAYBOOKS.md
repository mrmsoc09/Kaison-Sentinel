# Playbooks

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

OSINT playbooks live under `playbooks/osint/`.
Vulnerability playbooks live under `playbooks/vuln/`.
JSON playbook definitions (used by planner) live under `config/playbooks/`.

- `osint_recon_basic.yaml`
- `osint_recon_deep.yaml`

Each playbook is a sequence of modules (Module = Agent = Tool = Job).
Execution remains gated by scope and HiL.
MITRE planner maps techniques to playbook IDs for safe execution.
