# Kaison Sentinel Customization Guide (Safe Usage)

This guide explains how to customize MITRE-aligned assessment plans **without** implementing evasion, bypass, or destructive behavior.
Kaison Sentinel is built for authorized, defensive assessment and reporting.

## Principles
- **No destructive actions by default.**
- **Plan-first + HiL approval** required before any elevated or risky step.
- **Retain all intelligence** with lifecycle labels (raw → candidate → actionable/contextual → validated).
- **Evidence-first reporting** with redaction and audit trails.

## How to Extend the MITRE Planner
1. Edit `config/mitre_attack.json` and add techniques.
2. Use **safe objectives** and **read-only steps** only.
3. Keep scope + HiL gates intact.
4. Attach module playbooks under `playbooks` (osint/vuln/validation) to guide safe execution.

Example entry:
```json
{
  "technique_id": "TXXXX",
  "tactic_id": "TA000X",
  "tactic": "Example Tactic",
  "technique": "Example Technique",
  "safe_objective": "Assess exposure without altering target state.",
  "risk": "medium"
}
```

## Assessment Profiles (Multi-language)
The `lib/` folder contains **assessment profiles**, not exploit code.
These profiles are safe to run in restricted environments and are intended for:
- Evidence gathering
- Control inventory
- Report templating

Do **not** add disabling or bypass logic to these modules.

## Safe Customization Ideas
- Add environment-specific **read-only checks**.
- Enhance evidence templates and reporting fields.
- Integrate internal notifications (webhooks/audit logs) for result delivery.
- Add defensive validation checklists (policy drift, configuration integrity).

## Not Allowed
- Disabling or modifying security tools.
- Evasion, obfuscation, or bypass logic.
- Non-consensual or out-of-scope activities.

If you need help converting a requirement into a safe assessment plan, use the MITRE Planner and keep the **HiL gates** enabled.
