import json
from typing import Dict, Any
from pathlib import Path

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "policy_rules.json"


def _load_rules() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"deny": [], "require_hil_for_risk": []}


def requires_hil(risk: str) -> bool:
    rules = _load_rules()
    return risk in set(rules.get("require_hil_for_risk", []))


def allowed(role: str, action: str, module_kind: str, risk: str) -> bool:
    rules = _load_rules()
    for rule in rules.get("deny", []):
        if rule.get("action") and rule.get("action") != action:
            continue
        if rule.get("module_kind") and rule.get("module_kind") != module_kind:
            continue
        if rule.get("risk") and rule.get("risk") != risk:
            continue
        role_not_in = rule.get("role_not_in")
        if role_not_in and role not in role_not_in:
            return False
    return True
