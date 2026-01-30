from __future__ import annotations

from typing import Any, Dict, List
import re


SEV_MAP = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low",
    "info": "info",
    "informational": "info",
    "unknown": "info",
}


def _sev(value: Any) -> str:
    if not value:
        return "info"
    s = str(value).strip().lower()
    return SEV_MAP.get(s, "info")


def _conf_from_sev(sev: str) -> float:
    return {
        "critical": 0.9,
        "high": 0.8,
        "medium": 0.65,
        "low": 0.5,
        "info": 0.4,
    }.get(sev, 0.5)


def _safe_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(value)]


def _mk_finding(title: str, severity: str, target: str, evidence: List[Dict[str, str]],
                tool: str, labels: List[str] | None = None, confidence: float | None = None,
                status: str = "signal", signals: int = 1) -> Dict[str, Any]:
    labels = labels or []
    # Add CVE/CWE references when detected in title/labels
    cve_matches = re.findall(r"CVE-\\d{4}-\\d{4,7}", title, flags=re.IGNORECASE)
    for m in cve_matches:
        labels.append(m.upper())
    cwe_matches = re.findall(r"CWE-\\d{1,5}", title, flags=re.IGNORECASE)
    for m in cwe_matches:
        labels.append(m.upper())
    tool_label = f"tool:{tool}"
    if tool_label not in labels:
        labels.append(tool_label)
    return {
        "title": title,
        "severity": _sev(severity),
        "confidence": confidence if confidence is not None else _conf_from_sev(_sev(severity)),
        "target": target,
        "evidence": evidence,
        "status": status,
        "signals": signals,
        "labels": labels,
        "tool": tool,
    }


def parse_nuclei(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, list):
        return []
    findings: List[Dict[str, Any]] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        info = item.get("info") or {}
        title = info.get("name") or item.get("template-id") or "Nuclei finding"
        severity = info.get("severity") or "info"
        matched = item.get("matched-at") or item.get("host") or item.get("url") or target
        labels = []
        if item.get("template-id"):
            labels.append(f"template:{item.get('template-id')}")
        for t in _safe_list(info.get("tags")):
            labels.append(f"tag:{t}")
        if info.get("reference"):
            for ref in _safe_list(info.get("reference")):
                labels.append(f"ref:{ref}")
        if item.get("type"):
            labels.append(f"type:{item.get('type')}")
        findings.append(_mk_finding(
            title=title,
            severity=severity,
            target=str(matched),
            evidence=[{"kind": "nuclei", "path": str(matched)}],
            tool=tool,
            labels=labels,
        ))
    return findings


def parse_trivy(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for result in parsed.get("Results", []) or []:
        target_name = result.get("Target") or target
        vulns = result.get("Vulnerabilities") or []
        for v in vulns:
            vid = v.get("VulnerabilityID") or "Trivy finding"
            sev = v.get("Severity") or "info"
            pkg = v.get("PkgName") or "package"
            title = f"{vid} in {pkg}"
            labels = []
            if v.get("PrimaryURL"):
                labels.append(f"ref:{v.get('PrimaryURL')}")
            for ref in _safe_list(v.get("References")):
                labels.append(f"ref:{ref}")
            if vid:
                labels.append(f"cve:{vid}")
            evidence = [{"kind": "trivy", "path": str(target_name)}]
            findings.append(_mk_finding(title, sev, str(target_name), evidence, tool, labels=labels))
    return findings


def parse_grype(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for match in parsed.get("matches", []) or []:
        vuln = match.get("vulnerability") or {}
        artifact = match.get("artifact") or {}
        vid = vuln.get("id") or "Grype finding"
        sev = vuln.get("severity") or "info"
        pkg = artifact.get("name") or "package"
        ver = artifact.get("version") or ""
        title = f"{vid} in {pkg} {ver}".strip()
        labels = []
        if vid:
            labels.append(f"cve:{vid}")
        for ref in _safe_list(vuln.get("dataSource")):
            labels.append(f"ref:{ref}")
        evidence = [{"kind": "grype", "path": str(target)}]
        findings.append(_mk_finding(title, sev, target, evidence, tool, labels=labels))
    return findings


def parse_osv(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for res in parsed.get("results", []) or []:
        pkgs = res.get("packages") or []
        vulns = res.get("vulnerabilities") or []
        pkg_names = [p.get("package", {}).get("name") for p in pkgs if p.get("package")]
        pkg_label = ", ".join([p for p in pkg_names if p]) or "package"
        for v in vulns:
            vid = v.get("id") or "OSV finding"
            sev = v.get("severity") or v.get("database_specific", {}).get("severity") or "info"
            title = f"{vid} in {pkg_label}"
            labels = [f"cve:{vid}"] if vid else []
            for ref in _safe_list(v.get("references")):
                if isinstance(ref, dict) and ref.get("url"):
                    labels.append(f"ref:{ref.get('url')}")
                else:
                    labels.append(f"ref:{ref}")
            evidence = [{"kind": "osv", "path": str(target)}]
            findings.append(_mk_finding(title, sev, target, evidence, tool, labels=labels))
    return findings


def parse_npm_audit(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    vulns = parsed.get("vulnerabilities") or {}
    for name, v in vulns.items():
        sev = v.get("severity") or "info"
        title = f"npm audit: {name}"
        labels = []
        for via in v.get("via") or []:
            if isinstance(via, dict):
                if via.get("source"):
                    labels.append(f"ref:{via.get('url') or via.get('source')}")
                if via.get("title"):
                    labels.append(f"desc:{via.get('title')}")
            else:
                labels.append(f"ref:{via}")
        findings.append(_mk_finding(title, sev, target, [{"kind": "npm_audit", "path": str(target)}], tool, labels=labels))
    return findings


def parse_pip_audit(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, list):
        return []
    findings: List[Dict[str, Any]] = []
    for dep in parsed:
        name = dep.get("name") or "dependency"
        vulns = dep.get("vulns") or dep.get("vulnerabilities") or []
        for v in vulns:
            vid = v.get("id") or "pip-audit finding"
            sev = v.get("severity") or "medium"
            title = f"{vid} in {name}"
            labels = [f"cve:{vid}"] if vid else []
            findings.append(_mk_finding(title, sev, target, [{"kind": "pip_audit", "path": str(target)}], tool, labels=labels))
    return findings


def parse_semgrep(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for res in parsed.get("results", []) or []:
        extra = res.get("extra") or {}
        title = res.get("check_id") or extra.get("message") or "Semgrep finding"
        sev = extra.get("severity") or "info"
        path = res.get("path") or target
        labels = []
        for ref in _safe_list(extra.get("references")):
            labels.append(f"ref:{ref}")
        findings.append(_mk_finding(title, sev, str(path), [{"kind": "semgrep", "path": str(path)}], tool, labels=labels))
    return findings


def parse_bandit(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for res in parsed.get("results", []) or []:
        title = res.get("issue_text") or res.get("test_id") or "Bandit issue"
        sev = res.get("issue_severity") or "info"
        path = res.get("filename") or target
        confidence = _conf_from_sev(_sev(sev))
        if res.get("issue_confidence"):
            conf = str(res.get("issue_confidence")).lower()
            if conf == "high":
                confidence = min(1.0, confidence + 0.1)
            elif conf == "low":
                confidence = max(0.3, confidence - 0.1)
        findings.append(_mk_finding(title, sev, str(path), [{"kind": "bandit", "path": str(path)}], tool, confidence=confidence))
    return findings


def parse_gosec(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for res in parsed.get("Issues", []) or []:
        title = res.get("details") or res.get("rule_id") or "Gosec issue"
        sev = res.get("severity") or "info"
        path = res.get("file") or target
        findings.append(_mk_finding(title, sev, str(path), [{"kind": "gosec", "path": str(path)}], tool))
    return findings


def parse_tfsec(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for res in parsed.get("results", []) or []:
        title = res.get("description") or res.get("rule_id") or "tfsec finding"
        sev = res.get("severity") or "info"
        path = res.get("resource") or target
        findings.append(_mk_finding(title, sev, str(path), [{"kind": "tfsec", "path": str(path)}], tool))
    return findings


def parse_checkov(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    results = parsed.get("results") or {}
    for res in results.get("failed_checks", []) or []:
        title = res.get("check_name") or res.get("check_id") or "checkov finding"
        sev = res.get("severity") or "info"
        path = res.get("file_path") or target
        findings.append(_mk_finding(title, sev, str(path), [{"kind": "checkov", "path": str(path)}], tool))
    return findings


def parse_dependency_check(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    findings: List[Dict[str, Any]] = []
    for dep in parsed.get("dependencies", []) or []:
        vulns = dep.get("vulnerabilities") or []
        for v in vulns:
            vid = v.get("name") or v.get("source") or "dependency-check finding"
            sev = v.get("severity") or "info"
            title = f"{vid} in {dep.get('fileName', 'dependency')}"
            labels = []
            if v.get("name"):
                labels.append(f"cve:{v.get('name')}")
            findings.append(_mk_finding(title, sev, target, [{"kind": "dependency_check", "path": str(target)}], tool, labels=labels))
    return findings


def parse_generic_lines(parsed: Any, target: str, tool: str) -> List[Dict[str, Any]]:
    if not isinstance(parsed, list):
        return []
    findings: List[Dict[str, Any]] = []
    for line in parsed[:50]:
        if not isinstance(line, str):
            continue
        if "vulnerable" in line.lower() or "warning" in line.lower() or "critical" in line.lower():
            findings.append(_mk_finding(line[:140], "medium", target, [{"kind": tool, "path": "inline"}], tool))
    return findings
