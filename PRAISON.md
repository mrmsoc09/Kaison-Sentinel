# PRAISON.md — Kaison Sentinel OSINT/Recon Governance

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

These rules are injected into all PraisonAI agents.

## Scope & Safety
- Operate in **plan-first** mode. Execution requires explicit approval.
- Deny-by-default for any action outside the approved scope allowlist.
- No active exploitation. OSINT/Recon only unless a separate, approved vulnerability module is engaged.
- No outbound network calls unless explicitly allowed for the active run.

## Evidence & Reporting
- Evidence is mandatory before any item is marked **validated**.
- Evidence must include source pointers and capture metadata (timestamp, tool, operator).
- Human-in-the-loop approval is required for any high-risk or execute-mode action.

## Intelligence Lifecycle (No Deletion)
- **All intelligence is retained.** Nothing is deleted or discarded.
- Items are labeled with a lifecycle state:
  - `raw` → `candidate` → `actionable` → `validated`
  - `suppressed` exists only for scope-violating or clearly irrelevant items (retained, not deleted).
- State changes are permitted only when new evidence or context arrives.
- “Actionable” is a **label**, not a filter: it changes prioritization and routing, not retention.

## Data Isolation
- Cross-target contamination is forbidden. Intelligence for Target A must not influence Target B unless explicitly approved.
- Maintain separate memory/knowledge stores per target and per run.

## Redaction
- Redaction-first logging is mandatory for secrets and PII.
- Only summary outputs should include derived intelligence without raw sensitive strings.

