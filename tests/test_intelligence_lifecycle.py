from kai11.core.contracts import Finding, EvidenceRef
from kai11.core.intelligence_lifecycle import label_findings
from kai11.core.guardrails import apply_guardrails


def test_label_findings_actionable():
    f = Finding(
        id="f1",
        title="Leak",
        severity="high",
        confidence=0.9,
        target="example.com",
        evidence=[EvidenceRef(kind="raw", path="/tmp/x")],
        status="signal",
    )
    out = label_findings([f], {"allowlist": ["example.com"]})
    assert out[0].intel_state in {"actionable", "candidate", "validated"}
    assert out[0].scope_match is True


def test_guardrails_downgrade_without_hil():
    f = Finding(
        id="f2",
        title="Issue",
        severity="medium",
        confidence=0.8,
        target="example.com",
        evidence=[EvidenceRef(kind="raw", path="/tmp/y")],
        status="validated",
    )
    f.intel_state = "validated"
    out = apply_guardrails([f], {"validation_confirmed": False})
    assert out[0].intel_state == "actionable"
