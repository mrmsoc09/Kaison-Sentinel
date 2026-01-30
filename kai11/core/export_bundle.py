import json
from pathlib import Path
from typing import Dict, Any
import zipfile

from .config import OUTPUT_DIR, RUNS_DIR

EXPORT_DIR = OUTPUT_DIR / "exports"


def build_bundle(run_id: str) -> Dict[str, Any]:
    run_path = RUNS_DIR / f"{run_id}.json"
    if not run_path.exists():
        return {"status": "error", "reason": "run_not_found"}
    try:
        run = json.loads(run_path.read_text())
    except Exception:
        return {"status": "error", "reason": "run_unreadable"}

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    bundle_path = EXPORT_DIR / f"{run_id}_bundle.zip"
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as z:
        report_bundle = run.get("report_bundle") or {}
        for _, path in (report_bundle or {}).items():
            if path and Path(path).exists():
                z.write(path, arcname=Path(path).name)
        evidence_bundle = OUTPUT_DIR / "evidence" / f"{run_id}_bundle.json"
        if evidence_bundle.exists():
            z.write(evidence_bundle, arcname=evidence_bundle.name)
        attachments = OUTPUT_DIR / "evidence" / f"{run_id}_attachments.jsonl"
        if attachments.exists():
            z.write(attachments, arcname=attachments.name)
    return {"status": "ok", "path": str(bundle_path)}
