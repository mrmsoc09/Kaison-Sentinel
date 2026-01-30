from typing import List
from .contracts import Finding
from .report_formatter import format_report
from .prompt_manager import list_report_formats


def render_report(run_id: str, findings: List[Finding]) -> str:
    lines = [
        f"# Kaison Sentinel Report — {run_id}",
        "",
        "## Findings",
    ]
    if not findings:
        lines.append("No findings.")
        return "\n".join(lines)

    for f in findings:
        lines.append(f"### {f.title}")
        lines.append(f"- Severity: {f.severity}")
        lines.append(f"- Confidence: {round(f.confidence, 2)}")
        lines.append(f"- Target: {f.target}")
        lines.append(f"- Status: {f.status}")
        lines.append(f"- Intelligence State: {f.intel_state}")
        lines.append(f"- Scope Match: {f.scope_match}")
        lines.append(f"- Duplicate Risk: {f.duplicate_risk} (matches: {f.duplicate_matches}, validated: {f.duplicate_validated})")
        if f.labels:
            lines.append(f"- Labels: {', '.join(sorted(set(f.labels)))}")
        if f.repro_steps:
            lines.append("- Reproduction Steps:")
            for step in f.repro_steps:
                lines.append(f"  - {step}")
        lines.append("")
        if f.mitigation:
            lines.append("**Mitigation (tier: %s)**" % f.mitigation.tier)
            lines.append("Dry-run commands:")
            for c in f.mitigation.dry_run_cmds:
                lines.append(f"- `{c}`")
            lines.append("Apply commands:")
            for c in f.mitigation.apply_cmds:
                lines.append(f"- `{c}`")
            lines.append("Verify:")
            for s in f.mitigation.verify_steps:
                lines.append(f"- {s}")
            lines.append("Rollback:")
            for s in f.mitigation.rollback_steps:
                lines.append(f"- {s}")
            if f.mitigation.code_fix:
                lines.append("Code Fix:")
                lines.append(f"- {f.mitigation.code_fix}")
            lines.append("")
    return "\n".join(lines)


def render_report_with_format(run_id: str, findings: List[Finding], format_id: str | None = None, summary_override: str | None = None, context: dict | None = None) -> str:
    summary = summary_override or "Findings summary"
    mitigation = "See mitigation guidance for tiered steps."
    formatted = format_report(run_id, summary, [f.__dict__ for f in findings], mitigation, format_id=format_id, context=context)
    return formatted.get("content", "")


def render_report_bundle(run_id: str, findings: List[Finding], summary_override: str | None = None, context: dict | None = None) -> List[dict]:
    summary = summary_override or "Findings summary"
    mitigation = "See mitigation guidance for tiered steps."
    formats = list_report_formats() or [{"id": "report.md.default", "format": "md"}]
    bundle = []
    for fmt in formats:
        formatted = format_report(run_id, summary, [f.__dict__ for f in findings], mitigation, format_id=fmt.get("id"), context=context)
        bundle.append(formatted)
    return bundle
