# Lang Studio Implementation Notes

This build uses a lightweight LangStudio layer for local traces and evaluations.

- Traces: `kai11/langstudio/tracing.py` → `outputs/traces/`
- Evals: `kai11/langstudio/evals.py` → `outputs/langstudio/`
- LangGraph adapter: `kai11/langstudio/langgraph_runner.py` (uses LangGraph if installed, otherwise a deterministic offline graph)

These are offline-first adapters designed to run without network access. When LangGraph/LangSmith
dependencies are enabled, the adapters automatically use the real integrations.
