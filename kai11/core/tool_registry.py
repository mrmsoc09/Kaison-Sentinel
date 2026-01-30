import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "tool_registry.json"


def load_registry() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"version": 1, "defaults": {}, "categories": {}}


def category_meta(category: str) -> Dict[str, Any]:
    reg = load_registry()
    defaults = reg.get("defaults", {})
    meta = reg.get("categories", {}).get(category, {})
    out = dict(defaults)
    out.update(meta)
    return out
