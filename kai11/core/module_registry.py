import importlib
import json
from pathlib import Path
from typing import List, Dict, Any

from .config import BUILD_ROOT

REGISTRY_PATH = BUILD_ROOT / "modules" / "registry.json"


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"version": 1, "modules": []}
    return json.loads(REGISTRY_PATH.read_text())


def list_modules(kind: str | None = None) -> List[Dict[str, Any]]:
    reg = load_registry()
    mods = reg.get("modules", [])
    if not kind or kind == "all":
        return mods
    if kind == "osint":
        return [m for m in mods if m.get("kind") in {"osint", "recon"}]
    return [m for m in mods if m.get("kind") == kind]


def load_module(entry: str):
    mod_name, _, cls_name = entry.rpartition(":")
    if not mod_name or not cls_name:
        raise ValueError("module_entry_invalid")
    mod = importlib.import_module(mod_name)
    cls = getattr(mod, cls_name)
    return cls()
