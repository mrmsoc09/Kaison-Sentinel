from typing import List, Dict, Any
import json
from pathlib import Path

from .contracts import Finding


def _has_screen_recording(findings: List[Finding]) -> bool:
    for f in findings:
        for e in f.evidence:
            if e.kind in {"screen_recording", "screencast", "video"}:
                return True
    return False


def _attachments_have_screen_recording(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("kind") in {"screen_recording", "screencast", "video"}:
                    return True
    except Exception:
        return False
    return False


def report_preflight(
    findings: List[Finding],
    scope: Dict[str, Any],
    attachments_path: Path,
    module_kind: str,
) -> tuple[bool, str]:
    if module_kind != "vuln":
        return True, ""

    if scope.get("validation_confirmed") is not True:
        return False, "validation_not_confirmed"

    if scope.get("report_hil_confirmed") is not True:
        return False, "report_hil_not_confirmed"

    # Require screen recording for report readiness
    if not _has_screen_recording(findings) and not _attachments_have_screen_recording(attachments_path):
        return False, "screen_recording_missing"

    # Require evidence if any validated/likely findings exist
    validated = [f for f in findings if f.status in {"validated", "likely"}]
    if validated and not any(f.evidence for f in validated):
        return False, "evidence_missing"

    return True, ""
