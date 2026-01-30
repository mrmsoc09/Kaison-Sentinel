import json
from pathlib import Path
from kai11.langstudio.evals import evaluate_findings


def test_evaluate_findings_writes_file(tmp_path, monkeypatch):
    # Redirect output directory by monkeypatching module constant
    from kai11 import langstudio
    evals = langstudio.evals
    evals.LANGSTUDIO_DIR = tmp_path
    evals.LANGSTUDIO_DIR.mkdir(parents=True, exist_ok=True)

    findings = [{"id": "f1", "confidence": 0.9, "scope_match": True, "evidence": [1]}]
    path = evaluate_findings(findings, "run-1")
    p = Path(path)
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["run_id"] == "run-1"
