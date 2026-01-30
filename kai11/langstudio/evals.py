import json
from datetime import datetime
from typing import Dict, Any, List

from ..core.config import LANGSTUDIO_DIR

LANGSTUDIO_DIR.mkdir(parents=True, exist_ok=True)


def score_finding(item: Dict[str, Any]) -> Dict[str, Any]:
    evidence = item.get("evidence") or []
    confidence = float(item.get("confidence", 0.0))
    scope_match = bool(item.get("scope_match", True))
    score = 0.0
    if evidence:
        score += 0.4
    if confidence >= 0.75:
        score += 0.4
    if scope_match:
        score += 0.2
    return {
        "id": item.get("id"),
        "score": round(score, 2),
        "evidence_count": len(evidence),
        "scope_match": scope_match,
        "confidence": confidence,
    }


def evaluate_findings(findings: List[Dict[str, Any]], run_id: str) -> str:
    results = [score_finding(f) for f in findings]
    payload = {
        "run_id": run_id,
        "evaluated_at": datetime.utcnow().isoformat(),
        "results": results,
    }
    path = LANGSTUDIO_DIR / f"eval_{run_id}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return str(path)
