# OSINT Implementation Status

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

All OSINT tools are wired into the 1Tool/1Agent/1Job framework.

Execution behavior:
- Each tool runs via `core/tool_exec.py` using `config/tools_osint.json`.
- If the binary is missing, the tool returns `missing_binary`.
- If `KAI_ALLOW_NETWORK` is not set, the tool returns `blocked`.
- Active tools require `KAI_ALLOW_ACTIVE=1`.
- Hooks enforce pre/post checks and attach evidence metadata.
- Tool registry metadata supplies risk/evidence labels by category.
- OSINT workflows are defined in `.praison/workflows/`.
- OSINT artifacts are routed to training, vector store, and knowledge store.
- LangStudio traces/evals and BigQuery exports are generated per run.

This is a complete execution scaffold. Tool-specific flags and parsers can be tuned per tool by editing `config/tools_osint.json`.
