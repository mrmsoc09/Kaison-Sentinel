import json
from pathlib import Path

from kai11.core.evidence import write_evidence_bundle, verify_evidence_bundle


def test_evidence_immutability(tmp_path: Path):
    run_id = "test-run"
    items = [{"k": "v"}]
    path = write_evidence_bundle(run_id, items)
    assert verify_evidence_bundle(path) is True

    data = json.loads(Path(path).read_text())
    data["items"].append({"tamper": True})
    Path(path).write_text(json.dumps(data))
    assert verify_evidence_bundle(path) is False
