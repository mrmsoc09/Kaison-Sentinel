# DeepAgents Plan (OSINT/Recon)

Purpose: enable long-horizon, attacker-style chaining for OSINT/Recon.

Planned usage:
- DeepAgents planner generates investigation trees with explicit scope gates.
- Each branch maps to a 1Tool/1Agent/1Job execution step.
- Outputs feed into intelligence lifecycle labeling (raw → candidate → actionable/contextual).

Constraints:
- Plan-first + HiL approval before execute.
- No deletion; all outputs retained with labels.

Status:
- Offline planner is active; optional DeepAgents runtime can be enabled when dependency is installed.
