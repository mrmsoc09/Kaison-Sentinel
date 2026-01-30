from kai11.core.findings import dedupe_findings
from kai11.core.contracts import Finding, EvidenceRef


def test_dedupe_merges_signals_and_evidence():
    f1 = Finding(id="1", title="Issue", severity="high", confidence=0.6, target="t", evidence=[EvidenceRef(kind="a", path="1")], status="signal", signals=1)
    f2 = Finding(id="2", title="Issue", severity="high", confidence=0.8, target="t", evidence=[EvidenceRef(kind="b", path="2")], status="validated", signals=2)
    merged = dedupe_findings([f1, f2])
    assert len(merged) == 1
    assert merged[0].signals == 3
    assert merged[0].confidence == 0.8
    assert merged[0].status == "validated"
    assert len(merged[0].evidence) == 2
