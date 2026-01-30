# Lang Studio To-Do (Approval Required)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

This list is staged for approval and later execution.

## Core Integration
- [ ] Add LangSmith tracing and run metadata capture for OSINT/Recon
- [ ] Add LangGraph durable workflow runner for long OSINT jobs
- [ ] Add LangChain tool wrappers for OSINT pipeline steps
- [ ] Enable langstudio config toggles from `config/langstudio.json`

## Quality & Safety
- [ ] Add evaluation harness for OSINT findings (precision/recall proxy)
- [ ] Add HITL interrupts for risky steps
- [ ] Add sandboxed tool runner for untrusted tools

## DeepAgents (Approved for use)
- [ ] Integrate DeepAgents for long-horizon investigations
- [ ] Create DeepAgents planner with explicit scope and approval gates
- [ ] Bind DeepAgents outputs into intelligence lifecycle labeling

## Optional Integrations
- [ ] Haystack pipelines for retrieval + validation loops
- [ ] n8n workflow hooks for approvals/notifications

