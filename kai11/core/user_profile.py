import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

PROFILE_PATH = BUILD_ROOT / "config" / "user_profile.json"


def load_profile() -> Dict[str, Any]:
    if not PROFILE_PATH.exists():
        return {"email": "", "name": "", "org": ""}
    try:
        return json.loads(PROFILE_PATH.read_text())
    except Exception:
        return {"email": "", "name": "", "org": ""}


def save_profile(data: Dict[str, Any]) -> Dict[str, Any]:
    profile = load_profile()
    profile.update({k: v for k, v in data.items() if v is not None})
    PROFILE_PATH.write_text(json.dumps(profile, ensure_ascii=False, indent=2))
    return profile
