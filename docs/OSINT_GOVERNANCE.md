# OSINT/Recon Governance

## Principles
- Plan-first execution with explicit approvals.
- Deny-by-default for out-of-scope tools/targets.
- OSINT/Recon only (no active exploitation).
- Evidence-first reporting with HiL validation for “validated” items.
- Redaction-first logging.

## Intelligence Lifecycle (No Deletion)
All intelligence is retained. Items are labeled to control prioritization and routing:

- `raw`: untriaged data
- `candidate`: plausible but unverified
- `actionable`: prioritized for follow-up (label-only; never deletes data)
- `validated`: human-confirmed with evidence
- `contextual`: out-of-scope or weakly related but retained
- `suppressed`: legacy compatibility label (treated as contextual)

### Why this approach?
This avoids discarding early signals that may become actionable later, while still preventing
weak or unrelated data from influencing unrelated decisions while keeping it
available for later correlation.

## Suggested Metadata
Each intel item should include:
- `state`
- `confidence`
- `evidence` pointers
- `scope_match`
- `freshness` timestamp
- `related_targets` (if explicitly approved)
