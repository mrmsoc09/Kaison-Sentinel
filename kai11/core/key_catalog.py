import json
from typing import Dict, Any

from .config import BUILD_ROOT

CATALOG_PATH = BUILD_ROOT / "config" / "api_key_catalog.json"


def load_key_catalog() -> Dict[str, Any]:
    if not CATALOG_PATH.exists():
        return {"catalog": []}
    try:
        return json.loads(CATALOG_PATH.read_text())
    except Exception:
        return {"catalog": []}
