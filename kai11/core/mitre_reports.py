import json
import csv
import io
from typing import Dict, Any, List

from .config import BUILD_ROOT
from .storage import write_report
from .template import render_template
from .pdf_writer import render_pdf_from_text


def _load_formats() -> List[Dict[str, Any]]:
    fmt_dir = BUILD_ROOT / "config" / "mitre_report_formats"
    if not fmt_dir.exists():
        return []
    formats: List[Dict[str, Any]] = []
    for p in sorted(fmt_dir.glob("*.json")):
        try:
            formats.append(json.loads(p.read_text()))
        except Exception:
            continue
    return formats


def _steps_md(steps: List[Dict[str, Any]]) -> str:
    if not steps:
        return "- None"
    lines = []
    for step in steps:
        lines.append(f"- [{step.get('type')}] {step.get('description')}")
    return "\n".join(lines)


def _steps_html(steps: List[Dict[str, Any]]) -> str:
    if not steps:
        return "<li>None</li>"
    return "".join([f"<li><strong>{s.get('type')}</strong>: {s.get('description')}</li>" for s in steps])


def _render_csv(steps: List[Dict[str, Any]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["step_id", "type", "description"])
    for step in steps:
        writer.writerow([step.get("id"), step.get("type"), step.get("description")])
    return output.getvalue()


def render_mitre_bundle(plan: Dict[str, Any]) -> Dict[str, Any]:
    formats = _load_formats()
    steps = plan.get("steps") or []
    payload = {
        "technique_id": plan.get("technique_id"),
        "tactic_id": plan.get("tactic_id"),
        "tactic": plan.get("tactic"),
        "technique": plan.get("technique"),
        "objective": plan.get("objective"),
        "risk": plan.get("risk"),
        "gating": json.dumps(plan.get("gating"), ensure_ascii=False, indent=2),
        "muted_plan": json.dumps(plan.get("muted_plan"), ensure_ascii=False, indent=2),
        "playbooks_by_module": json.dumps(plan.get("playbooks_by_module", {}), ensure_ascii=False, indent=2),
        "recommended_playbooks": ", ".join(plan.get("recommended_playbooks") or []) or "None",
        "report_templates": ", ".join(plan.get("report_templates") or []) or "None",
        "steps_md": _steps_md(steps),
        "steps_html": _steps_html(steps),
    }

    if not formats:
        formats = [
            {"id": "mitre_plan_md", "format": "md", "template": "# MITRE Plan {technique_id}\n\n{steps_md}\n"}
        ]

    report_paths: Dict[str, str] = {}
    for fmt in formats:
        fmt_type = (fmt.get("format") or "md").lower()
        report_id = fmt.get("id") or "mitre_plan"
        run_id = f"mitre_{plan.get('technique_id','plan').replace('.', '_')}_{report_id}"
        if fmt_type == "json":
            content = json.dumps(plan, ensure_ascii=False, indent=2)
        elif fmt_type == "csv":
            content = _render_csv(steps)
        elif fmt_type == "pdf":
            pdf_text = (
                f"MITRE Plan {plan.get('technique_id')}\n\n"
                f"Tactic: {plan.get('tactic_id')} {plan.get('tactic')}\n"
                f"Technique: {plan.get('technique')}\n\n"
                f"Objective: {plan.get('objective')}\nRisk: {plan.get('risk')}\n\n"
                f"Steps:\n{_steps_md(steps)}\n\n"
                f"Gating:\n{plan.get('gating')}\n"
            )
            content = render_pdf_from_text(pdf_text)
        else:
            content = render_template(fmt.get("template", ""), payload)
        ext = "md" if fmt_type == "md" else fmt_type
        report_paths[fmt_type] = write_report(run_id, content, ext=ext)

    return {
        "report_bundle": report_paths,
        "report_templates": [f.get("id") for f in formats],
    }
