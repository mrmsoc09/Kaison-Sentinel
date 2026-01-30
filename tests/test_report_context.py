from kai11.core.report_context import build_report_context
from kai11.core.contracts import Finding, EvidenceRef


def test_report_context_basic():
    findings = [
        Finding(id="1", title="XSS", severity="high", confidence=0.8, target="example.com", evidence=[], status="signal"),
        Finding(id="2", title="SQLi", severity="critical", confidence=0.9, target="example.com", evidence=[], status="signal", labels=["CWE-89"]),
    ]
    scope = {"allowlist": ["example.com"], "constraints": "plan-first", "allowed_techniques": ["passive"]}
    ctx = build_report_context(scope, assets=["example.com"], findings=findings, module_kind="vuln")
    assert "Targets: example.com" in ctx["scope_summary"]
    assert ctx["severity_counts"]["critical"] == 1
    assert "CWE-89" in ctx["compliance"]
