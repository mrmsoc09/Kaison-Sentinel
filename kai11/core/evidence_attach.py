import json
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR

ATTACH_DIR = OUTPUT_DIR / "evidence"
ATTACH_DIR.mkdir(parents=True, exist_ok=True)


def attach_evidence(run_id: str, finding_id: str, kind: str, path: str) -> Dict[str, Any]:
    ATTACH_DIR.mkdir(parents=True, exist_ok=True)
    record = {"run_id": run_id, "finding_id": finding_id, "kind": kind, "path": path}
    out = ATTACH_DIR / f"{run_id}_attachments.jsonl"
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {"status": "ok", "path": str(out)}
