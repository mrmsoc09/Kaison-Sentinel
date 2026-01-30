from kai11.core.vuln_parsers import parse_nuclei, parse_trivy


def test_parse_nuclei_basic():
    parsed = [
        {"template-id": "xss", "matched-at": "https://example.com", "info": {"name": "XSS", "severity": "high", "tags": ["xss"]}},
    ]
    findings = parse_nuclei(parsed, "example.com", "tool.nuclei")
    assert len(findings) == 1
    assert findings[0]["severity"] == "high"
    assert any("tool:tool.nuclei" in lbl for lbl in findings[0]["labels"])


def test_parse_trivy_basic():
    parsed = {
        "Results": [
            {"Target": "image:latest", "Vulnerabilities": [{"VulnerabilityID": "CVE-123", "Severity": "MEDIUM", "PkgName": "openssl"}]}
        ]
    }
    findings = parse_trivy(parsed, "image:latest", "tool.trivy")
    assert findings
    assert findings[0]["title"].startswith("CVE-123")
