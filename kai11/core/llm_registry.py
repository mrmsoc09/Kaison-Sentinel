import json
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "llm_profiles.json"


def load_llm_profiles() -> Dict[str, Any]:
    if not CONF.exists():
        return {"providers": []}
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"providers": []}
