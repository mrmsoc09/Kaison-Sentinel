# Lang Studio Integration Plan (Approved)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Intent
- Add durable orchestration (LangGraph)
- Add observability & evaluation (LangSmith)
- Add structured tool wrappers (LangChain)

## Implementation Notes
- Current build uses offline-first adapters for tracing/evals and a LangGraph-compatible runner.
- When LangGraph/LangSmith dependencies are enabled, adapters switch to real integrations automatically.

## Safe Defaults
- No network calls by default
- All executions gated by HiL + scope
