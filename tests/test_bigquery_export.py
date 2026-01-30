from pathlib import Path
from kai11.core.bigquery_export import export_bigquery_payload


def test_bigquery_export_writes_files(tmp_path, monkeypatch):
    from kai11 import core
    export_mod = core.bigquery_export
    export_mod.BQ_DIR = tmp_path

    artifacts = [{"type": "endpoint", "value": "/admin", "confidence": 0.6, "module": "m", "tool": "t", "target": "example.com", "timestamp": "now"}]
    findings = [{"id": "f1", "title": "Issue", "severity": "low", "confidence": 0.5, "target": "example.com", "status": "signal", "intel_state": "candidate", "scope_match": True, "labels": []}]
    out = export_bigquery_payload("run-1", {"allowlist": ["example.com"]}, artifacts, findings, "/tmp/report.md", "", [], training_path=None)
    paths = out["paths"]
    assert Path(paths["artifacts"]).exists()
    assert Path(paths["findings"]).exists()
    assert Path(paths["reports"]).exists()
