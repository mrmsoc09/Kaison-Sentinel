import json
from pathlib import Path

from kai11.core.duplicate_risk import apply_duplicate_risk
from kai11.core.contracts import Finding, EvidenceRef
from kai11.core.config import RUNS_DIR


def test_duplicate_risk_scoring(tmp_path):
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    prior = {
        "run_id": "run-20000101-000000",
        "findings": [
            {"id": "a", "title": "XSS", "severity": "high", "target": "example.com", "status": "validated"}
        ],
    }
    p = RUNS_DIR / "run-20000101-000000.json"
    p.write_text(json.dumps(prior))
    findings = [
        Finding(id="b", title="XSS", severity="high", confidence=0.5, target="example.com", evidence=[], status="signal"),
        Finding(id="c", title="Info", severity="info", confidence=0.2, target="example.com", evidence=[], status="signal"),
    ]
    out = apply_duplicate_risk(findings, "run-29990101-000000")
    assert out[0].duplicate_risk in {"medium", "high"}
