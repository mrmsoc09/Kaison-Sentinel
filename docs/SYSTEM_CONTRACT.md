# Kaison Sentinel System Contract (No Upsell Scope)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Core Principles
- Offline by default; no external calls unless explicitly enabled and approved.
- Safety-first: deny-by-default on execute, HiL approvals required.
- Evidence-first: no VALIDATED finding without screen recording reference.
- Mitigation is mandatory for every validated finding.

## Canonical Pipeline
1) Plan
2) Execute (gated)
3) Parse
4) Normalize
5) Triage
6) Validate (HiL)
7) Report
8) Mitigate (mandatory output)

## Governance Rules
- Scope must be explicit and verifiable.
- Safe mode is default for risky tools (e.g., Metasploit).
- No destructive actions and no automatic execution on external systems.
- All agent actions and decisions must be logged.

## Mitigation Output Requirements
Each validated finding must include:
- Minimal / Standard / Deep remediation tier
- Read-only (dry-run) commands first
- Apply commands only after HiL approval
- Verification steps
- Rollback guidance
- Rotation steps for any secrets/keys/tokens
- Cloud CLI steps for: GCP, AWS, Azure, Cloudflare

## Platforms
- Primary OS: Ubuntu/Debian
- Cloud: GCP, AWS, Azure, Cloudflare (first-class CLI guidance)

## Technical Requirements
6. Include docstrings for each Adapter class explaining the "Strategic Intent":
   - GoogleSCCAdapter: "Purpose: Provide visibility to Cloud Governance teams."
   - AWSSecurityHubAdapter: "Purpose: Enable automated Lambda-based remediation."
   - SarifAdapter: "Purpose: Provide line-of-code feedback to developers in PRs."

## Non-Goals (for this build)
- No marketplace/upsell features
- No autonomous external execution without explicit approvals
