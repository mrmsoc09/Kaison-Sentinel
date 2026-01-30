import json
from pathlib import Path
from typing import Dict, Any

from ..core.config import BUILD_ROOT
from ..core.audit import append_audit

CONF = BUILD_ROOT / "config" / "vertex_ai.json"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False}


def submit_training_job(dataset_uri: str) -> Dict[str, Any]:
    conf = _load_conf()
    if not conf.get("enabled"):
        return {"status": "disabled"}

    try:
        from google.cloud import aiplatform  # type: ignore
        from google.auth import load_credentials_from_file  # type: ignore
    except Exception:
        return {"status": "missing_dependency", "dependency": "google-cloud-aiplatform"}

    project_id = conf.get("project_id")
    region = conf.get("region")
    pipeline_spec_uri = conf.get("pipeline_spec_uri")
    staging_bucket = conf.get("staging_bucket")
    training_pipeline = conf.get("training_pipeline", "kai-training")
    sa_json = conf.get("service_account_json")

    if not project_id or not region or not pipeline_spec_uri:
        return {"status": "error", "reason": "missing_config"}

    credentials = None
    if sa_json:
        credentials, _ = load_credentials_from_file(sa_json)

    aiplatform.init(project=project_id, location=region, staging_bucket=staging_bucket, credentials=credentials)
    job = aiplatform.PipelineJob(
        display_name=training_pipeline,
        template_path=pipeline_spec_uri,
        parameter_values={"dataset_uri": dataset_uri},
    )
    job.submit()
    append_audit({"event": "vertex_train_submitted", "dataset_uri": dataset_uri, "pipeline": training_pipeline})
    return {"status": "submitted", "pipeline": training_pipeline}
