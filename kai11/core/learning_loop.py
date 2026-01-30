import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from .config import OUTPUT_DIR
from .contracts import Finding
from ..vector.embed import embed_text

TRAINING_JSONL = OUTPUT_DIR / "training_data.jsonl"
TRAINING_VEC = OUTPUT_DIR / "training_vector_store.jsonl"


def _example_from_finding(run_id: str, scope: Dict[str, Any], finding: Finding) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "target": finding.target,
        "title": finding.title,
        "severity": finding.severity,
        "confidence": finding.confidence,
        "labels": finding.labels,
        "status": finding.status,
        "signals": finding.signals,
        "intel_state": finding.intel_state,
        "scope": scope.get("allowlist", []),
        "budget_tier": scope.get("budget_tier"),
        "stealth": scope.get("stealth"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def record_training_examples(run_id: str, scope: Dict[str, Any], findings: List[Finding]) -> Dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    with TRAINING_JSONL.open("a", encoding="utf-8") as out_json, TRAINING_VEC.open("a", encoding="utf-8") as out_vec:
        for f in findings:
            ex = _example_from_finding(run_id, scope, f)
            out_json.write(json.dumps(ex, ensure_ascii=False) + "\n")
            vec = embed_text(f"{f.title} {f.severity} {' '.join(f.labels)}")
            out_vec.write(json.dumps({
                "id": f"{run_id}:{f.id}",
                "text": f"{f.title} {f.severity}",
                "vector": vec,
                "meta": {"severity": f.severity, "status": f.status},
            }, ensure_ascii=False) + "\n")
            count += 1
    return {"status": "ok", "count": count, "path": str(TRAINING_JSONL)}
