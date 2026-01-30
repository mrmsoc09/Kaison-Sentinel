import json
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR, RUNS_DIR
from .email_sender import send_email

EMAIL_DIR = OUTPUT_DIR / "emails"
EMAIL_DIR.mkdir(parents=True, exist_ok=True)


def queue_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    EMAIL_DIR.mkdir(parents=True, exist_ok=True)
    if payload.get("hil_confirmed") is not True:
        return {"status": "blocked", "reason": "hil_required"}
    run_id = payload.get("run_id", "unknown")
    subject = payload.get("subject", "Kaison Sentinel report")
    to = payload.get("to", [])
    body = payload.get("body", "")
    html_body = payload.get("html_body", "")
    attachments = payload.get("attachments") or []
    if run_id and not attachments:
        run_path = RUNS_DIR / f"{run_id}.json"
        if run_path.exists():
            try:
                run = json.loads(run_path.read_text())
                report_bundle = run.get("report_bundle") or {}
                if isinstance(report_bundle, dict):
                    attachments = [p for p in report_bundle.values() if p]
            except Exception:
                pass
    out = {
        "run_id": run_id,
        "to": to,
        "subject": subject,
        "body": body,
        "html_body": html_body,
        "attachments": attachments,
    }
    send_result = send_email(out)
    out["send_result"] = send_result
    path = EMAIL_DIR / f"{run_id}_email.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    return {"status": "queued", "path": str(path), "send": send_result}
