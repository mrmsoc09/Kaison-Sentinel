---
description: OSINT/Recon governance and intelligence lifecycle
activation: always
---

# OSINT/Recon Governance

- Plan-first. Execution requires explicit approval.
- Deny-by-default for out-of-scope targets, tools, or data sources.
- No active exploitation in OSINT/Recon runs.
- All intelligence is retained; never delete or discard.

## Intelligence Lifecycle

Every intel item must carry:
- `state` (raw | candidate | actionable | validated | suppressed)
- `confidence` (0.0–1.0)
- `evidence` (source pointers or artifacts)
- `scope_match` (true/false)
- `freshness` (timestamp)

State transitions require new evidence or context. “Actionable” is a prioritization label only.

## Data Isolation

- No cross-target leakage of intelligence or memory.
- Separate memory/knowledge stores per target and run.

