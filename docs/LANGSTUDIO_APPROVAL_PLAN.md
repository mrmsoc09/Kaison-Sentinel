# Lang Studio Integration Plan (Approved)

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
