import json
from typing import Dict, Any
from pathlib import Path

from .config import BUILD_ROOT
from .policy_engine import requires_hil

CONF = BUILD_ROOT / "config" / "policy.json"


def _load_policy() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"defaults": {"allow_network": False, "allow_active": False, "hil_required": True, "safe_mode": True}}


def should_require_hil(mode: str, risk: str) -> bool:
    if mode != "execute":
        return False
    return requires_hil(risk)


def enforce_scope(scope: Dict) -> bool:
    # Deny-by-default when no allowlist is provided
    allowlist = scope.get("allowlist") or []
    return bool(allowlist)


def policy_defaults() -> Dict[str, Any]:
    return _load_policy().get("defaults", {})
