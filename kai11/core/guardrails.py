from typing import Dict, Any, List
from .contracts import Finding


def apply_guardrails(findings: List[Finding], scope: Dict[str, Any]) -> List[Finding]:
    # No deletions; only label adjustments
    for f in findings:
        if f.intel_state == "actionable" and (not f.evidence or not f.scope_match):
            f.intel_state = "candidate"
            if "downgraded_missing_evidence" not in f.labels:
                f.labels.append("downgraded_missing_evidence")
        if f.intel_state == "validated" and not scope.get("validation_confirmed"):
            f.intel_state = "actionable"
            if "downgraded_missing_hil" not in f.labels:
                f.labels.append("downgraded_missing_hil")
    return findings
