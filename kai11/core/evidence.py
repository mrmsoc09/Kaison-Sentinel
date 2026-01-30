import json
import hashlib
from pathlib import Path
from typing import List, Dict
from .config import OUTPUT_DIR

EVIDENCE_DIR = OUTPUT_DIR / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_evidence_bundle(run_id: str, items: List[Dict]) -> str:
    bundle = {
        "run_id": run_id,
        "items": items,
    }
    raw = json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8")
    digest = _sha256_bytes(raw)
    bundle["sha256"] = digest
    path = EVIDENCE_DIR / f"{run_id}_bundle.json"
    path.write_bytes(json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8"))
    return str(path)


def verify_evidence_bundle(path: str) -> bool:
    p = Path(path)
    if not p.exists():
        return False
    data = json.loads(p.read_text())
    digest = data.get("sha256")
    bundle = {"run_id": data.get("run_id"), "items": data.get("items")}
    raw = json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8")
    return digest == _sha256_bytes(raw)
