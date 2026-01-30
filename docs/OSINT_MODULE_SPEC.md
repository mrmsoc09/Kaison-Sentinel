# OSINT Module Spec (Module=1 Agent=1 Tool=1 Job)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## OSINT/DNS Lookup
- Module: `osint.dns_lookup`
- Agent: `agent.osint_dns`
- Tool: `tool.dns_lookup`
- Job: `job.dns_lookup`

## Orchestration
- Circle orchestration for OSINT:
  - Gemini + PraisonAI
  - Codex + PraisonAI
  - Claude + PraisonAI
- LangStudio cycle enabled: LangChain + LangGraph + LangSmith

## Execution
- Requires `KAI_ALLOW_NETWORK=1`
- Uses DNS resolution only (safe, low‑risk)

## Outputs
- `results`: DNS resolution details
- `assets`: resolved IP list
- Audit logs for circle and agent lifecycle
