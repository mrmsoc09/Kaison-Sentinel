import json
import os
import secrets
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT
from .audit import append_audit

CONF = BUILD_ROOT / "config" / "keys.json"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"mode": "env", "key_env": "KAI_ENCRYPTION_KEY"}


def get_active_key() -> str | None:
    conf = _load_conf()
    mode = conf.get("mode", "env")
    if mode == "env":
        return os.getenv(conf.get("key_env", "KAI_ENCRYPTION_KEY"))
    if mode == "file":
        key_file = conf.get("key_file")
        if key_file:
            p = BUILD_ROOT / key_file
            if p.exists():
                return p.read_text().strip()
    return None


def rotate_key(new_key: str | None = None) -> Dict[str, Any]:
    conf = _load_conf()
    mode = conf.get("mode", "env")
    new_key = new_key or secrets.token_hex(32)

    if mode == "env":
        append_audit({"event": "key_rotation", "mode": mode, "status": "env_only"})
        return {"status": "env_only", "key": new_key, "key_env": conf.get("key_env", "KAI_ENCRYPTION_KEY")}

    key_file = conf.get("key_file")
    if not key_file:
        return {"status": "error", "reason": "key_file_not_configured"}

    p = BUILD_ROOT / key_file
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(new_key)
    append_audit({"event": "key_rotation", "mode": mode, "key_file": str(p)})
    return {"status": "ok", "key_file": str(p)}
