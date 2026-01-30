from typing import Dict, Any, List
from datetime import datetime


def normalize_artifacts(module_id: str, tool_id: str, output_kind: str, parsed: Any, target: str, run_id: str | None = None) -> List[Dict[str, Any]]:
    now = datetime.utcnow().isoformat()
    artifacts: List[Dict[str, Any]] = []
    if parsed is None:
        return artifacts

    if isinstance(parsed, list):
        for item in parsed:
            artifacts.append({
                "type": output_kind,
                "value": item,
                "confidence": 0.6,
                "module": module_id,
                "tool": tool_id,
                "target": target,
                "run_id": run_id,
                "timestamp": now,
            })
    elif isinstance(parsed, dict):
        artifacts.append({
            "type": output_kind,
            "value": parsed,
            "confidence": 0.6,
            "module": module_id,
            "tool": tool_id,
            "target": target,
            "run_id": run_id,
            "timestamp": now,
        })
    else:
        artifacts.append({
            "type": output_kind,
            "value": parsed,
            "confidence": 0.6,
            "module": module_id,
            "tool": tool_id,
            "target": target,
            "run_id": run_id,
            "timestamp": now,
        })
    return artifacts
