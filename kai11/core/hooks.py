import json
from datetime import datetime
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "hooks.json"


def _load() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"version": 1, "pre": {}, "post": {}}


def before_tool(tool_id: str, target: str, meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
    cfg = _load().get("pre", {})
    if cfg.get("enforce_target_nonempty", False) and not target:
        return {"allowed": False, "reason": "empty_target"}
    return {"allowed": True}


def after_tool(tool_id: str, target: str, result: Dict[str, Any]) -> Dict[str, Any]:
    cfg = _load().get("post", {})
    if cfg.get("attach_evidence_meta", False):
        result.setdefault("evidence_meta", {})
        result["evidence_meta"].update({
            "tool_id": tool_id,
            "target": target,
            "captured_at": datetime.utcnow().isoformat(),
        })
    return result
