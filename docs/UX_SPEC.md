# UI/UX Specification (Kaison Sentinel)

## Objectives
- Maximize validated findings and minimize false positives.
- Make scope, approvals, and evidence unmissable.
- Provide mitigation guidance in-line with findings.

## Core Screens
1) Mission Control Dashboard
- System health, scan queue, running tools
- Active approvals and policy gates

2) Scope & Policy Panel (global, persistent)
- Scope allowlist/denylist
- Execution mode toggle (always gated)
- Safe-mode indicator

3) Findings Board
- Severity + confidence ladder
- Evidence and screen recording link
- Mitigation block with tier selector

4) Evidence Locker
- Immutable evidence bundles
- Audit trail per finding

5) Workflow Builder
- Drag-and-drop modules
- Plan-only preview before execution

6) Persona Console
- Agent actions and reasoning summary
- HiL approval points

## Visual Direction
- Base: Graphite #0F1115
- Primary: Steel #1C2128
- Accent success: Teal #12B5A6
- Accent warn: Amber #F1B84B
- Critical: Crimson #D14B4B
- Text: Mist #D9DEE7
- Muted: Slate #8C96A6

## UX Rules
- No pure white backgrounds
- Reduced-motion preference honored
- Tablet-first layout (768–1024px)
- Evidence-first workflows

## Mitigation UX
- Tier selector (Minimal/Standard/Deep)
- Show dry-run commands first
- Apply commands behind approval gate
- Verification + rollback steps inline
