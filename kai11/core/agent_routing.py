import json
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "agent_routing.json"


def _load() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"default_persona": "persona.security_analyst", "rules": []}


def select_persona(context: Dict[str, Any]) -> str:
    data = _load()
    for rule in data.get("rules", []):
        cond = rule.get("if", {})
        ok = True
        for k, v in cond.items():
            if context.get(k) != v:
                ok = False
                break
        if ok:
            return rule.get("persona") or data.get("default_persona")
    return data.get("default_persona")
