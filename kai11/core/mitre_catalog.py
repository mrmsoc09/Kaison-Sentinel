import json
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "mitre_attack.json"


def load_catalog() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"version": 1, "techniques": []}


def get_technique(technique_id: str) -> Dict[str, Any] | None:
    catalog = load_catalog()
    for t in catalog.get("techniques", []):
        if t.get("technique_id") == technique_id:
            return t
    return None
