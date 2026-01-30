from typing import Dict, Any, List
import csv
import io
import json

from .prompt_manager import list_report_formats
from .template import render_template
from .pdf_writer import render_pdf_from_text
from .findings import SEVERITY_ORDER


def _extract_refs(labels: List[str]) -> Dict[str, List[str]]:
    refs = {"cve": [], "cwe": [], "owasp": []}
    for l in labels:
        low = l.lower()
        if low.startswith("cve-"):
            refs["cve"].append(l)
        elif low.startswith("cwe-"):
            refs["cwe"].append(l)
        elif low.startswith("owasp"):
            refs["owasp"].append(l)
    return refs


def _risk_timeline(severity: str) -> str:
    if severity == "critical":
        return "Mitigate within 24-72 hours"
    if severity == "high":
        return "Mitigate within 7 days"
    if severity == "medium":
        return "Mitigate within 30 days"
    if severity == "low":
        return "Mitigate within 90 days"
    return "Mitigate as capacity allows"


def _format_finding(f: Dict[str, Any]) -> str:
    lines = [f"### {f.get('title')} ({f.get('severity')})"]
    lines.append(f"- Confidence: {round(float(f.get('confidence', 0)), 2)}")
    lines.append(f"- Status: {f.get('status')}")
    if f.get("reportability") is not None:
        rep = round(float(f.get("reportability", 0.0)), 1)
        lines.append(f"- Reportability: {rep}")
    if f.get("duplicate_risk"):
        lines.append(f"- Duplicate Risk: {f.get('duplicate_risk')} (matches: {f.get('duplicate_matches', 0)}, validated: {f.get('duplicate_validated', 0)})")
    if f.get("signals"):
        lines.append(f"- Signals: {f.get('signals')}")
    lines.append(f"- Timeline: {_risk_timeline((f.get('severity') or 'info').lower())}")
    labels = f.get("labels") or []
    refs = _extract_refs(labels)
    if any(refs.values()):
        lines.append("- References:")
        if refs["owasp"]:
            lines.append(f"  - OWASP: {', '.join(refs['owasp'])}")
        if refs["cwe"]:
            lines.append(f"  - CWE: {', '.join(refs['cwe'])}")
        if refs["cve"]:
            lines.append(f"  - CVE: {', '.join(refs['cve'])}")
    if f.get("repro_steps"):
        lines.append("- Reproduction Steps:")
        for step in f.get("repro_steps"):
            lines.append(f"  - {step}")
    ev = f.get("evidence") or []
    if ev:
        lines.append("- Evidence:")
        for e in ev:
            lines.append(f"  - {e.get('kind')}: {e.get('path')}")
    mit = f.get("mitigation") or {}
    if mit:
        lines.append("- Mitigation:")
        for c in mit.get("dry_run_cmds", []):
            lines.append(f"  - dry-run: {c}")
        for c in mit.get("apply_cmds", []):
            lines.append(f"  - apply: {c}")
        for s in mit.get("verify_steps", []):
            lines.append(f"  - verify: {s}")
        for s in mit.get("rollback_steps", []):
            lines.append(f"  - rollback: {s}")
        if mit.get("code_fix"):
            lines.append("  - code-fix:")
            lines.append(f"    {mit.get('code_fix')}")
    return "\n".join(lines)


def _render_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _render_sarif(payload: Dict[str, Any]) -> str:
    findings = payload.get("findings", [])
    results = []
    for f in findings:
        results.append({
            "ruleId": f.get("id") or f.get("title"),
            "level": f.get("severity"),
            "message": {"text": f.get("title")},
        })
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {"driver": {"name": "Kaison Sentinel"}},
                "results": results,
            }
        ],
    }
    return json.dumps(sarif, ensure_ascii=False, indent=2)


def _render_csv(findings: List[Dict[str, Any]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id",
        "title",
        "severity",
        "confidence",
        "status",
        "reportability",
        "duplicate_risk",
        "duplicate_matches",
        "duplicate_validated",
        "signals",
        "evidence",
        "mitigation",
    ])
    for f in findings:
        evidence_items = f.get("evidence") or []
        evidence = "; ".join([f"{e.get('kind')}:{e.get('path')}" for e in evidence_items])
        mitigation = f.get("mitigation") or {}
        mitigation_steps = []
        mitigation_steps += [f"dry-run:{c}" for c in mitigation.get("dry_run_cmds", [])]
        mitigation_steps += [f"apply:{c}" for c in mitigation.get("apply_cmds", [])]
        mitigation_steps += [f"verify:{s}" for s in mitigation.get("verify_steps", [])]
        mitigation_steps += [f"rollback:{s}" for s in mitigation.get("rollback_steps", [])]
        if mitigation.get("code_fix"):
            mitigation_steps.append(f"code-fix:{mitigation.get('code_fix')}")
        writer.writerow([
            f.get("id"),
            f.get("title"),
            f.get("severity"),
            f.get("confidence"),
            f.get("status"),
            f.get("reportability"),
            f.get("duplicate_risk"),
            f.get("duplicate_matches"),
            f.get("duplicate_validated"),
            f.get("signals"),
            evidence,
            " | ".join(mitigation_steps),
        ])
    return output.getvalue()

def format_report(run_id: str, summary: str, findings: List[Dict[str, Any]], mitigation: str, format_id: str | None = None, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    formats = list_report_formats()
    fmt = formats[0] if formats else {"id": "default", "format": "md", "template": "{summary}\n{findings}\n"}
    if format_id:
        for f in formats:
            if f.get("id") == format_id:
                fmt = f
                break

    severity_order = {s: i for i, s in enumerate(SEVERITY_ORDER)}
    findings_sorted = sorted(findings, key=lambda f: severity_order.get((f.get("severity") or "info").lower(), 99), reverse=True)
    findings_text = "\n\n".join([_format_finding(f) for f in findings_sorted]) or "No findings."
    ctx = context or {}
    severity_counts = ctx.get("severity_counts", {})
    scope_summary = ctx.get("scope_summary", "")
    methodology = ctx.get("methodology", "")
    assets_inventory = ctx.get("assets_inventory", [])
    compliance = ctx.get("compliance", [])
    risk_matrix = ctx.get("risk_matrix", "")
    payload = {
        "run_id": run_id,
        "summary": summary,
        "scope_summary": scope_summary,
        "methodology": methodology,
        "assets_inventory": "\n".join([f"- {a}" for a in assets_inventory]) or "No assets recorded.",
        "severity_counts": severity_counts,
        "risk_matrix": risk_matrix,
        "compliance": "\n".join([f"- {c}" for c in compliance]) or "No compliance mappings.",
        "findings": findings_text,
        "mitigation": mitigation,
        "evidence": "See findings for evidence references.",
        "findings_raw": findings_sorted,
        "mitre_context": ctx.get("mitre_context", "None"),
        "playbook_context": ctx.get("playbook_context", "None"),
        "validation_recommendation": ctx.get("validation_recommendation", ""),
    }

    if fmt.get("format") == "json":
        return {"format": "json", "content": _render_json(payload), "id": fmt.get("id")}
    if fmt.get("format") == "sarif":
        return {"format": "sarif", "content": _render_sarif(payload), "id": fmt.get("id")}
    if fmt.get("format") == "csv":
        return {"format": "csv", "content": _render_csv(findings), "id": fmt.get("id")}
    if fmt.get("format") == "pdf":
        pdf_text = (
            f"Kaison Sentinel Report {run_id}\n\n"
            f"Executive Summary\n{summary}\n\n"
            f"Scope & Methodology\n{scope_summary}\n\n{methodology}\n\n"
            f"Asset Inventory\n{payload.get('assets_inventory')}\n\n"
            f"MITRE Context\n{payload.get('mitre_context')}\n\n"
            f"Playbooks\n{payload.get('playbook_context')}\n\n"
            f"Validation Recommendation\n{payload.get('validation_recommendation')}\n\n"
            f"Risk Matrix\n{risk_matrix}\n\n"
            f"Findings (by severity)\n{findings_text}\n\n"
            f"Mitigation\n{mitigation}\n\n"
            f"Compliance Mapping\n{payload.get('compliance')}\n"
        )
        return {"format": "pdf", "content": render_pdf_from_text(pdf_text), "id": fmt.get("id")}

    rendered = render_template(fmt.get("template", ""), payload)
    return {"format": fmt.get("format"), "content": rendered, "id": fmt.get("id")}
