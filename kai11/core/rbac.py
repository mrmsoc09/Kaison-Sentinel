import json
from pathlib import Path
from typing import List

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "policy.json"


def _load_roles():
    try:
        return json.loads(CONF.read_text()).get("roles", {})
    except Exception:
        return {}


def has_permission(role: str, perm: str) -> bool:
    roles = _load_roles()
    return perm in roles.get(role, [])


def permissions(role: str) -> List[str]:
    roles = _load_roles()
    return roles.get(role, [])
