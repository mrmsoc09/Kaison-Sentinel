import json
from pathlib import Path
from typing import Dict, Any, List

from .config import OUTPUT_DIR
from .contracts import Finding


def compute_metrics(findings: List[Finding]) -> Dict[str, Any]:
    if not findings:
        return {"findings": 0, "avg_confidence": 0.0, "avg_reportability": 0.0}
    avg_conf = sum(f.confidence for f in findings) / len(findings)
    avg_rep = sum(getattr(f, "reportability", 0.0) for f in findings) / len(findings)
    sev = {}
    for f in findings:
        sev[f.severity] = sev.get(f.severity, 0) + 1
    return {
        "findings": len(findings),
        "avg_confidence": round(avg_conf, 3),
        "avg_reportability": round(avg_rep, 3),
        "by_severity": sev,
    }


def write_metrics(run_id: str, findings: List[Finding]) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{run_id}_metrics.json"
    path.write_text(json.dumps(compute_metrics(findings), ensure_ascii=False, indent=2))
    return str(path)
