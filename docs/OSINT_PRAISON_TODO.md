# OSINT/Recon — PraisonAI Implementation Checklist

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Governance & Policy
- [x] PRAISON.md rules file
- [x] `.praison/rules/` governance rules
- [x] Intelligence lifecycle policy (retain all data)

## Tooling Architecture (1 Tool / 1 Agent / 1 Job)
- [x] Tool registry metadata (risk/evidence)
- [x] Hooks for pre/post tool execution

## Workflows
- [x] YAML workflows for discovery/enumeration/exposure/attribution/triage

## Guardrails
- [x] Guardrails for evidence/HiL without deletion
- [x] Lifecycle labeling for intelligence

## Knowledge & Memory
- [x] Knowledge store for OSINT artifacts

## Auditable Outputs
- [x] Report includes intelligence state
- [x] Run record includes lifecycle policy reference

