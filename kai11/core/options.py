import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "options_master.json"
OVERRIDE = BUILD_ROOT / "config" / "options_override.json"


def _load_master() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"shared": {}}


def _load_override() -> Dict[str, Any]:
    try:
        return json.loads(OVERRIDE.read_text())
    except Exception:
        return {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def get_options(kind: str) -> Dict[str, Any]:
    master = _load_master()
    shared = master.get("shared", {})
    override = _load_override()
    if kind in {"osint", "recon"}:
        return _deep_merge(_deep_merge(shared, master.get("osint_overrides", {})), override)
    if kind == "vuln":
        return _deep_merge(_deep_merge(shared, master.get("vuln_overrides", {})), override)
    if kind == "validation":
        return _deep_merge(_deep_merge(shared, master.get("validation_overrides", {})), override)
    return _deep_merge(shared, override)


def save_override(data: Dict[str, Any]) -> Dict[str, Any]:
    current = _load_override()
    merged = _deep_merge(current, data)
    OVERRIDE.write_text(json.dumps(merged, ensure_ascii=False, indent=2))
    return merged
