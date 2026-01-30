import json
import os
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "api_auth.json"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False, "header": "X-API-Key", "keys": []}


def auth_enabled() -> bool:
    if os.getenv("KAI_API_AUTH") == "1":
        return True
    return bool(_load_conf().get("enabled", False))


def header_name() -> str:
    return _load_conf().get("header", "X-API-Key")


def validate_api_key(key: str | None) -> Dict[str, Any]:
    if not auth_enabled():
        return {"status": "disabled"}
    if not key:
        return {"status": "missing"}
    for rec in _load_conf().get("keys", []):
        if rec.get("key") == key:
            return {
                "status": "ok",
                "role": rec.get("role", "viewer"),
                "tenant_id": rec.get("tenant_id", "default"),
                "key_id": rec.get("id", "unknown"),
            }
    return {"status": "invalid"}
