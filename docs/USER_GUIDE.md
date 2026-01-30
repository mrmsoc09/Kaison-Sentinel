# User Guide (Operator)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

See `docs/USER_CHECKLIST.md` for the full options checklist.

1) Open UI at `http://localhost:7878`
2) (Optional) Use **MITRE Planner** to auto‑fill playbooks + technique
3) Fill **Guided Plan** (goal + targets + budget/stealth + playbook IDs)
4) (Optional) Refresh program scope cache
   - `KAI_ALLOW_NETWORK=1 python3 scripts/fetch_program_guidelines.py --allow-network`
   - Or use **Setup Hub → Program scopes cache → Sync now**
5) Parse scope cache into allowlists (Scheduler panel → Parse Scope Cache)
6) Review plan output (ensure scope + modules are correct)
7) Execute only after HiL approval
8) Attach evidence (include screen recording)
9) Generate report bundle
10) Draft email + HiL confirm send

Optional setup:
- Use **Platform Options** to set vault backend, DB settings, and active LLM provider.
- Add LLM keys via **Key Vault (OSINT)** using source IDs (e.g., `source.openai`).
