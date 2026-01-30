import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

SETUP_PATH = BUILD_ROOT / "config" / "setup_hub.json"


def load_setup_hub() -> Dict[str, Any]:
    if not SETUP_PATH.exists():
        return {"steps": []}
    try:
        return json.loads(SETUP_PATH.read_text())
    except Exception:
        return {"steps": []}


def update_setup_step(step_id: str, status: str) -> Dict[str, Any]:
    data = load_setup_hub()
    steps = data.get("steps", [])
    for step in steps:
        if step.get("id") == step_id:
            step["status"] = status
            break
    SETUP_PATH.write_text(json.dumps({"steps": steps}, ensure_ascii=False, indent=2))
    return {"steps": steps}
