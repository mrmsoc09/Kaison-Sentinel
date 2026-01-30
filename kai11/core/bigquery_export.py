import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from .config import OUTPUT_DIR, BUILD_ROOT

BQ_DIR = OUTPUT_DIR / "bigquery"
SCHEMA_PATH = BUILD_ROOT / "config" / "bigquery_schema.json"


def _load_schema() -> Dict[str, Any]:
    try:
        return json.loads(SCHEMA_PATH.read_text())
    except Exception:
        return {"tables": {}}


def _validate_rows(table: str, rows: List[Dict[str, Any]]) -> List[str]:
    schema = _load_schema().get("tables", {}).get(table, [])
    if not schema:
        return []
    missing = []
    for col in schema:
        for r in rows:
            if col not in r:
                missing.append(col)
                break
    return sorted(set(missing))


def _jsonl_write(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def export_bigquery_payload(
    run_id: str,
    scope: Dict[str, Any],
    artifacts: List[Dict[str, Any]],
    findings: List[Dict[str, Any]],
    report_path: str,
    eval_path: str | None,
    module_exec: List[Dict[str, Any]],
    training_path: str | None = None,
) -> Dict[str, Any]:
    now = datetime.utcnow().isoformat()
    target = (scope.get("allowlist") or [""])[0]
    tenant_id = scope.get("tenant_id", "")

    artifact_rows: List[Dict[str, Any]] = []
    for a in artifacts:
        val = a.get("value")
        if not isinstance(val, str):
            val = json.dumps(val, ensure_ascii=False)
        artifact_rows.append({
            "run_id": run_id,
            "tenant_id": tenant_id,
            "target": a.get("target", target),
            "type": a.get("type"),
            "value": val,
            "confidence": a.get("confidence", 0.0),
            "module": a.get("module"),
            "tool": a.get("tool"),
            "timestamp": a.get("timestamp"),
        })

    finding_rows: List[Dict[str, Any]] = []
    evidence_rows: List[Dict[str, Any]] = []
    for f in findings:
        finding_rows.append({
            "run_id": run_id,
            "tenant_id": tenant_id,
            "finding_id": f.get("id"),
            "title": f.get("title"),
            "severity": f.get("severity"),
            "confidence": f.get("confidence"),
            "target": f.get("target"),
            "status": f.get("status"),
            "intel_state": f.get("intel_state"),
            "scope_match": f.get("scope_match"),
            "reportability": f.get("reportability", 0.0),
            "duplicate_risk": f.get("duplicate_risk", "low"),
            "duplicate_matches": f.get("duplicate_matches", 0),
            "duplicate_validated": f.get("duplicate_validated", 0),
            "labels": ",".join(sorted(set(f.get("labels", [])))),
            "created_at": f.get("created_at"),
        })
        for ev in f.get("evidence") or []:
            evidence_rows.append({
                "run_id": run_id,
                "tenant_id": tenant_id,
                "finding_id": f.get("id"),
                "kind": ev.get("kind"),
                "path": ev.get("path"),
            })

    trace_rows: List[Dict[str, Any]] = []
    for m in module_exec:
        flow = m.get("flow") or {}
        if flow.get("trace"):
            trace_rows.append({
                "run_id": run_id,
                "tenant_id": tenant_id,
                "module": m.get("module"),
                "trace_path": flow.get("trace"),
                "summary": flow.get("summary"),
            })

    report_rows = [{
        "run_id": run_id,
        "tenant_id": tenant_id,
        "target": target,
        "report_path": report_path,
        "eval_path": eval_path or "",
        "created_at": now,
    }]

    training_rows = []
    if training_path:
        training_rows.append({
            "run_id": run_id,
            "tenant_id": tenant_id,
            "path": training_path,
            "created_at": now,
        })

    payload = {
        "artifacts": artifact_rows,
        "findings": finding_rows,
        "evidence": evidence_rows,
        "traces": trace_rows,
        "reports": report_rows,
        "training": training_rows,
    }

    validation = {
        "artifacts": _validate_rows("artifacts", artifact_rows),
        "findings": _validate_rows("findings", finding_rows),
        "evidence": _validate_rows("evidence", evidence_rows),
        "traces": _validate_rows("traces", trace_rows),
        "reports": _validate_rows("reports", report_rows),
        "training": _validate_rows("training", training_rows),
    }

    _jsonl_write(BQ_DIR / f"{run_id}_artifacts.jsonl", artifact_rows)
    _jsonl_write(BQ_DIR / f"{run_id}_findings.jsonl", finding_rows)
    _jsonl_write(BQ_DIR / f"{run_id}_evidence.jsonl", evidence_rows)
    _jsonl_write(BQ_DIR / f"{run_id}_traces.jsonl", trace_rows)
    _jsonl_write(BQ_DIR / f"{run_id}_reports.jsonl", report_rows)
    if training_rows:
        _jsonl_write(BQ_DIR / f"{run_id}_training.jsonl", training_rows)

    return {
        "payload": payload,
        "validation": validation,
        "paths": {
            "artifacts": str(BQ_DIR / f"{run_id}_artifacts.jsonl"),
            "findings": str(BQ_DIR / f"{run_id}_findings.jsonl"),
            "evidence": str(BQ_DIR / f"{run_id}_evidence.jsonl"),
            "traces": str(BQ_DIR / f"{run_id}_traces.jsonl"),
            "reports": str(BQ_DIR / f"{run_id}_reports.jsonl"),
            "training": str(BQ_DIR / f"{run_id}_training.jsonl") if training_rows else "",
        }
    }
