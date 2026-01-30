import json
from pathlib import Path
from typing import Dict, Any

from ..core.config import BUILD_ROOT
from ..core.audit import append_audit

CONF = BUILD_ROOT / "config" / "bigquery.json"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False}


def load_to_bigquery(payload: Dict[str, Any]) -> Dict[str, Any]:
    conf = _load_conf()
    if not conf.get("enabled"):
        return {"status": "disabled"}

    try:
        from google.cloud import bigquery  # type: ignore
    except Exception:
        return {"status": "missing_dependency", "dependency": "google-cloud-bigquery"}

    project_id = conf.get("project_id")
    dataset_id = conf.get("dataset_id") or conf.get("dataset")
    tables = conf.get("tables", {})
    if not project_id or not dataset_id or not tables:
        return {"status": "error", "reason": "missing_config"}

    sa_path = conf.get("service_account_json") or ""
    if sa_path:
        client = bigquery.Client.from_service_account_json(sa_path, project=project_id)
    else:
        client = bigquery.Client(project=project_id)
    results = {}
    for key, table_name in tables.items():
        rows = payload.get(key)
        if not rows:
            continue
        if isinstance(rows, dict):
            rows = [rows]
        table_ref = f"{project_id}.{dataset_id}.{table_name}"
        errors = client.insert_rows_json(table_ref, rows)
        results[key] = {"table": table_ref, "errors": errors or []}
    append_audit({"event": "bigquery_load", "tables": list(results.keys())})
    return {"status": "ok", "results": results}
