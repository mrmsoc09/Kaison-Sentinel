import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "programs.json"


def _load_programs() -> Dict[str, Any]:
    if not CONF.exists():
        return {"programs": []}
    return json.loads(CONF.read_text())


def list_programs() -> list[Dict[str, Any]]:
    data = _load_programs()
    return data.get("programs", [])


def get_program(program_id: str | None) -> Dict[str, Any]:
    data = _load_programs()
    for p in data.get("programs", []):
        if p.get("id") == program_id:
            return p
    return {}
