import json
from pathlib import Path
from typing import Dict, Any, List

from .config import RUNS_DIR


def _counts(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = (f.get("severity") or "info").lower()
        counts[sev] = counts.get(sev, 0) + 1
    return counts


def list_runs(limit: int = 25) -> List[Dict[str, Any]]:
    items = sorted(RUNS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    out = []
    for p in items[:limit]:
        try:
            data = json.loads(p.read_text())
            findings = data.get("findings", []) or []
            out.append({
                "run_id": data.get("run_id"),
                "mode": data.get("mode"),
                "tenant_id": data.get("tenant_id", ""),
                "created_at": data.get("created_at") or data.get("scope", {}).get("validation_confirmed_at"),
                "findings_count": len(findings),
                "severity_counts": _counts(findings),
                "report_bundle": data.get("report_bundle") or {},
            })
        except Exception:
            out.append({"run_id": p.stem, "status": "unreadable_or_encrypted"})
    return out
