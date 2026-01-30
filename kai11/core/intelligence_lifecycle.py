import json
from typing import Dict, Any, List

from .config import BUILD_ROOT
from .contracts import Finding

CONF = BUILD_ROOT / "config" / "intelligence_lifecycle.json"


def load_policy() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"version": 1, "states": {}, "labels": {}}


def _scope_match(target: str, allowlist: List[str]) -> bool:
    if not allowlist:
        return True
    for a in allowlist:
        if not a:
            continue
        if target == a or target.endswith(a) or a in target:
            return True
    return False


def label_findings(findings: List[Finding], scope: Dict[str, Any]) -> List[Finding]:
    allowlist = scope.get("allowlist") or []
    for f in findings:
        f.scope_match = _scope_match(f.target, allowlist)
        f.freshness = f.created_at
        state = "raw"
        if not f.scope_match:
            state = "contextual"
            if "out_of_scope" not in f.labels:
                f.labels.append("out_of_scope")
        elif f.status == "validated":
            state = "validated"
        elif f.evidence and f.confidence >= 0.75:
            state = "actionable"
        else:
            state = "candidate"
        f.intel_state = state
        if state not in f.labels:
            f.labels.append(state)
    return findings
