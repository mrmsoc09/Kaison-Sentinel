import json
from pathlib import Path
from typing import List

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "validation_checks.json"


def validation_checklist() -> List[str]:
    if not CONF.exists():
        return []
    return json.loads(CONF.read_text()).get("checks", [])
