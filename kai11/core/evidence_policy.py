from typing import List, Dict, Any

from .contracts import Finding
from .audit import append_audit


def enforce_screen_recording(findings: List[Finding], scope: Dict[str, Any]) -> List[Finding]:
    screen = scope.get("screen_recording")
    for f in findings:
        if f.status != "validated":
            continue
        has_ev = any(e.kind == "screen_recording" for e in f.evidence)
        if not screen and not has_ev:
            f.status = "signal"
            append_audit({"event": "downgrade_validation", "reason": "missing_screen_recording", "finding": f.id})
    return findings


def enforce_evidence_required(findings: List[Finding]) -> List[Finding]:
    for f in findings:
        if f.status != "validated":
            continue
        if not f.evidence:
            f.status = "signal"
            append_audit({"event": "downgrade_validation", "reason": "missing_evidence", "finding": f.id})
    return findings
