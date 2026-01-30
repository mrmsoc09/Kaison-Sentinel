from typing import Dict, Any, List

from .contracts import Finding
from .findings import SEVERITY_ORDER
from .mitre_catalog import get_technique


def _severity_counts(findings: List[Finding]) -> Dict[str, int]:
    counts = {s: 0 for s in SEVERITY_ORDER}
    for f in findings:
        sev = (f.severity or "info").lower()
        if sev not in counts:
            counts[sev] = 0
        counts[sev] += 1
    return counts


def _risk_matrix(counts: Dict[str, int]) -> str:
    lines = [
        "Severity | Count | Recommended Response",
        "---------|-------|----------------------",
    ]
    response = {
        "critical": "Immediate (24-72h)",
        "high": "Urgent (<=7d)",
        "medium": "Planned (<=30d)",
        "low": "Backlog (<=90d)",
        "info": "As capacity allows",
    }
    for sev in ["critical", "high", "medium", "low", "info"]:
        lines.append(f"{sev} | {counts.get(sev, 0)} | {response.get(sev)}")
    return "\n".join(lines)


def _compliance_map(findings: List[Finding]) -> List[str]:
    refs = set()
    for f in findings:
        for label in f.labels:
            low = label.lower()
            if low.startswith("cve-") or low.startswith("cwe-") or low.startswith("owasp"):
                refs.add(label)
    return sorted(refs)


def _validation_recommendation(counts: Dict[str, int]) -> str:
    if counts.get("critical", 0) or counts.get("high", 0):
        return "Run validation playbook (playbook.vuln.validation) with HiL evidence gates."
    if counts.get("medium", 0):
        return "Consider validation playbook for medium findings with evidence collection."
    return "Validation playbook optional; continue with normal evidence collection."


def build_report_context(scope: Dict[str, Any], assets: List[str], findings: List[Finding], module_kind: str) -> Dict[str, Any]:
    counts = _severity_counts(findings)
    targets = ", ".join(scope.get("allowlist", []))
    constraints = scope.get("constraints", "")
    techniques = ", ".join(scope.get("allowed_techniques", []))
    scope_summary = f"Targets: {targets}\nModule: {module_kind}\nConstraints: {constraints}\nAllowed techniques: {techniques}"
    methodology = "Plan-first workflow; policy gating; HiL validation for execute and report; evidence required for validated findings."
    assets_inventory = sorted(set(assets)) if assets else []
    compliance = _compliance_map(findings)
    mitre_id = scope.get("mitre_technique_id") or ""
    mitre_context = ""
    if mitre_id:
        tech = get_technique(mitre_id) or {}
        mitre_context = f"{mitre_id} — {tech.get('tactic_id','')} {tech.get('tactic','')} · {tech.get('technique','')}".strip()
    playbook_ids = scope.get("playbook_ids") or []
    if isinstance(playbook_ids, str):
        playbook_ids = [p.strip() for p in playbook_ids.split(",") if p.strip()]
    playbook_context = ", ".join(playbook_ids) if playbook_ids else "None"
    budget = scope.get("budget_tier") or "standard"
    stealth = scope.get("stealth") or "standard"
    daily_budget = scope.get("daily_budget_usd")
    return {
        "severity_counts": counts,
        "scope_summary": scope_summary,
        "methodology": methodology,
        "assets_inventory": assets_inventory,
        "risk_matrix": _risk_matrix(counts),
        "compliance": compliance,
        "mitre_context": mitre_context or "None",
        "playbook_context": playbook_context,
        "validation_recommendation": _validation_recommendation(counts),
        "scan_profile": f"budget={budget}, stealth={stealth}, daily_budget_usd={daily_budget}",
    }
