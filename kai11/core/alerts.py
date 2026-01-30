from typing import List, Dict, Any
from pathlib import Path
import json

from .contracts import Finding
from .config import OUTPUT_DIR
from .notifications import queue_email
from .webhooks import post_webhook

ALERTS_DIR = OUTPUT_DIR / "alerts"
ALERTS_DIR.mkdir(parents=True, exist_ok=True)


def _counts(findings: List[Finding]) -> Dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        if not getattr(f, "scope_match", True):
            continue
        sev = (f.severity or "info").lower()
        if sev not in counts:
            sev = "info"
        counts[sev] += 1
    return counts


def _select_level(counts: Dict[str, int], thresholds: Dict[str, str]) -> str | None:
    if counts.get("critical", 0) or counts.get("high", 0):
        return thresholds.get("high", "instant")
    if counts.get("medium", 0):
        return thresholds.get("medium", "batch")
    if counts.get("low", 0) or counts.get("info", 0):
        return thresholds.get("low", "digest")
    return None


def maybe_alert(findings: List[Finding], options: Dict[str, Any], run_id: str, module_kind: str, scope: Dict[str, Any]) -> Dict[str, Any] | None:
    alerts = options.get("alerts", {}) if options else {}
    if not alerts.get("enabled", False):
        return None
    counts = _counts(findings)
    level = _select_level(counts, alerts.get("thresholds", {}))
    if not level:
        return None

    payload = {
        "run_id": run_id,
        "module_kind": module_kind,
        "level": level,
        "counts": counts,
        "top": [
            {"id": f.id, "title": f.title, "severity": f.severity, "target": f.target}
            for f in findings
            if f.severity in {"critical", "high", "medium"}
        ][:10],
    }
    path = ALERTS_DIR / f"{run_id}_alert.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    to = alerts.get("email_to") or scope.get("alert_to") or []
    if isinstance(to, str):
        to = [t.strip() for t in to.split(",") if t.strip()]
    if to:
        queue_email({
            "run_id": run_id,
            "to": to,
            "subject": f"Kaison Sentinel {module_kind} alert: {counts}",
            "body": json.dumps(payload, ensure_ascii=False, indent=2),
            "hil_confirmed": True,
        })

    post_webhook("alert.raised", payload)
    return {"level": level, "path": str(path), "counts": counts}


def maybe_hil_alert(cadence: Dict[str, Any], options: Dict[str, Any], run_id: str, scope: Dict[str, Any]) -> Dict[str, Any] | None:
    if cadence.get("status") != "overdue":
        return None
    payload = {
        "run_id": run_id,
        "type": "hil_cadence_overdue",
        "cadence": cadence,
    }
    path = ALERTS_DIR / f"{run_id}_hil_overdue.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    alerts = options.get("alerts", {}) if options else {}
    to = alerts.get("email_to") or scope.get("alert_to") or []
    if isinstance(to, str):
        to = [t.strip() for t in to.split(",") if t.strip()]
    if to:
        queue_email({
            "run_id": run_id,
            "to": to,
            "subject": "Kaison Sentinel HiL cadence overdue",
            "body": json.dumps(payload, ensure_ascii=False, indent=2),
            "hil_confirmed": True,
        })
    post_webhook("hil.overdue", payload)
    return {"path": str(path), "status": "overdue"}
