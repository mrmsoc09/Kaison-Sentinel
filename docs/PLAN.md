# Overall Plan (Structure‑First)

## Goal
Build a secure, modular, governed scanning platform that produces validated findings with actionable mitigation, while minimizing false positives.

## Structure
- **Modules**: plug‑and‑play scanners and recon tools
- **Governance**: policy gates, scope enforcement, HiL approvals
- **Evidence**: immutable, auditable, screen‑recorded validation
- **Mitigation**: mandatory, tiered, cloud‑aware remediation output
- **Data + DL**: BigQuery storage + Google DL (Vertex AI) for training and retrieval

## Execution Flow
1) Intake scope + constraints
2) Plan (module selection + risk classification)
3) Execute (gated)
4) Parse + normalize
5) Triage + correlation
6) Validate (HiL + evidence)
7) Report
8) Mitigate (tiered output)

## Primary Outcomes
- High‑confidence findings
- Low false‑positive rate
- Clear remediation and verification steps
- Full auditability
- BigQuery‑backed analytics and optional DL training loop
