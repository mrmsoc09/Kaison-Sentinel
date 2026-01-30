from typing import Dict, Any, List

from .vuln_parsers import (
    parse_nuclei,
    parse_trivy,
    parse_grype,
    parse_osv,
    parse_npm_audit,
    parse_pip_audit,
    parse_semgrep,
    parse_bandit,
    parse_gosec,
    parse_tfsec,
    parse_checkov,
    parse_dependency_check,
    parse_generic_lines,
)


def normalize_vuln_result(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Map common tool outputs to a finding schema when possible."""
    tool = result.get("tool")
    parsed = result.get("parsed")
    target = result.get("target") or result.get("host") or "unknown"

    if tool == "tool.nuclei":
        return parse_nuclei(parsed, target, tool)
    if tool == "tool.trivy":
        return parse_trivy(parsed, target, tool)
    if tool == "tool.grype":
        return parse_grype(parsed, target, tool)
    if tool == "tool.osv_scanner":
        return parse_osv(parsed, target, tool)
    if tool == "tool.npm_audit":
        return parse_npm_audit(parsed, target, tool)
    if tool == "tool.pip_audit":
        return parse_pip_audit(parsed, target, tool)
    if tool == "tool.semgrep":
        return parse_semgrep(parsed, target, tool)
    if tool == "tool.bandit":
        return parse_bandit(parsed, target, tool)
    if tool == "tool.gosec":
        return parse_gosec(parsed, target, tool)
    if tool == "tool.tfsec":
        return parse_tfsec(parsed, target, tool)
    if tool == "tool.checkov":
        return parse_checkov(parsed, target, tool)
    if tool == "tool.dependency_check":
        return parse_dependency_check(parsed, target, tool)

    # Generic fallback for noisy CLI tools
    if tool in {"tool.nikto", "tool.sqlmap", "tool.zap_cli", "tool.arachni", "tool.xsstrike", "tool.wpscan"}:
        return parse_generic_lines(parsed, target, tool)

    if tool == "tool.nmap_vuln" and isinstance(parsed, list):
        return [{
            "title": "Nmap vuln script: open service detected",
            "severity": "low",
            "confidence": 0.55,
            "target": target,
            "evidence": [{"kind": "nmap", "path": "inline"}],
            "status": "signal",
            "signals": max(1, len(parsed)),
            "labels": [f"ports:{','.join(parsed[:5])}"] if parsed else [],
            "tool": tool,
        }]

    return []
