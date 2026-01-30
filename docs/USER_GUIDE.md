# User Guide (Operator)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

See `docs/USER_CHECKLIST.md` for the full options checklist.

1) Open UI at `http://localhost:7878`
2) (Optional) Use **MITRE Planner** to auto‑fill playbooks + technique
3) Fill **Guided Plan** (goal + targets + playbook IDs)
4) (Optional) Refresh program scope cache
   - `python3 scripts/fetch_program_guidelines.py`
5) Review plan output (ensure scope + modules are correct)
6) Execute only after HiL approval
7) Attach evidence (include screen recording)
8) Generate report bundle
9) Draft email + HiL confirm send
