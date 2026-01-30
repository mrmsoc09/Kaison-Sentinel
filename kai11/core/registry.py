import json
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT

REGISTRY_DIR = BUILD_ROOT / "config"


def _load_dir(subdir: str) -> List[Dict[str, Any]]:
    root = REGISTRY_DIR / subdir
    if not root.exists():
        return []
    items = []
    for p in sorted(root.glob("*.json")):
        try:
            items.append(json.loads(p.read_text()))
        except Exception:
            continue
    return items


def load_prompts() -> List[Dict[str, Any]]:
    return _load_dir("prompts")


def load_personas() -> List[Dict[str, Any]]:
    return _load_dir("personas")


def load_playbooks() -> List[Dict[str, Any]]:
    return _load_dir("playbooks")


def load_report_formats() -> List[Dict[str, Any]]:
    return _load_dir("report_formats")


def load_agents() -> List[Dict[str, Any]]:
    return _load_dir("agents")


def load_personas_praison() -> List[Dict[str, Any]]:
    return _load_dir("personas_praison")


def load_personas_langstudio() -> List[Dict[str, Any]]:
    return _load_dir("personas_langstudio")
