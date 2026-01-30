import json
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT, RUNS_DIR
from .template import render_template
from .user_profile import load_profile

TEMPLATE_PATH = BUILD_ROOT / "config" / "prompts" / "email.vuln.v1.json"
TEMPLATE_HTML_PATH = BUILD_ROOT / "config" / "prompts" / "email.vuln.html.json"


def _load_template() -> str:
    if TEMPLATE_PATH.exists():
        try:
            data = json.loads(TEMPLATE_PATH.read_text())
            return data.get("content", "")
        except Exception:
            return ""
    return ""

def _load_template_html() -> str:
    if TEMPLATE_HTML_PATH.exists():
        try:
            data = json.loads(TEMPLATE_HTML_PATH.read_text())
            return data.get("content", "")
        except Exception:
            return ""
    return ""

def _load_run(run_id: str) -> Dict[str, Any] | None:
    # Only supports plaintext .json runs; encrypted runs require operator to decrypt externally.
    p = RUNS_DIR / f"{run_id}.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return None
    return None


def _summarize_findings(run: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = run.get("findings", []) or []
    out = []
    for f in findings[:5]:
        out.append({
            "title": f.get("title"),
            "severity": f.get("severity"),
            "confidence": f.get("confidence"),
            "target": f.get("target"),
            "reportability": f.get("reportability"),
            "duplicate_risk": f.get("duplicate_risk"),
        })
    return out


def _severity_breakdown(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = (f.get("severity") or "info").lower()
        if sev not in counts:
            counts[sev] = 0
        counts[sev] += 1
    return counts


def draft_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    run_id = payload.get("run_id")
    if not run_id:
        return {"status": "error", "error": "run_id_required"}

    run = _load_run(run_id)
    if not run:
        return {"status": "error", "error": "run_not_found_or_encrypted"}

    profile = load_profile()
    template = _load_template()
    template_html = _load_template_html()
    if not template:
        template = (
            "Hello {stakeholder_name},\n\n"
            "We have completed validation for the report {run_id}. Below is a concise summary "
            "of the validated findings and evidence attached.\n\n"
            "Findings: {findings_summary}\n\n"
            "Reproduction is included in the report, along with mitigation steps. "
            "Please evaluate the payout per program policy and severity guidance.\n\n"
            "Thank you,\n{sender_name}\n"
        )

    findings_summary = _summarize_findings(run)
    severity_breakdown = _severity_breakdown(run.get("findings", []) or [])
    action_items = [f.get("title") for f in (run.get("findings", []) or []) if (f.get("severity") or "").lower() in {"critical", "high"}][:5]
    values = {
        "stakeholder_name": payload.get("stakeholder_name", "Security Team"),
        "run_id": run_id,
        "findings_summary": json.dumps(findings_summary, ensure_ascii=False),
        "severity_breakdown": json.dumps(severity_breakdown, ensure_ascii=False),
        "action_items": json.dumps(action_items, ensure_ascii=False),
        "sender_name": profile.get("name") or payload.get("sender_name", "Kaison Sentinel Operator"),
        "org": profile.get("org", ""),
    }
    body = render_template(template, values)
    html_body = render_template(template_html, values) if template_html else ""

    subject = payload.get("subject") or f"Security Report {run_id}"
    to = payload.get("to") or []
    if isinstance(to, str):
        to = [t.strip() for t in to.split(",") if t.strip()]

    report_bundle = run.get("report_bundle") or {}
    attachments = [p for p in report_bundle.values() if p] if isinstance(report_bundle, dict) else []
    return {
        "status": "ok",
        "run_id": run_id,
        "to": to,
        "subject": subject,
        "body": body,
        "html_body": html_body,
        "attachments": attachments,
        "policy": "Respectful, evidence-first, no payout inflation; align with program policy.",
    }
