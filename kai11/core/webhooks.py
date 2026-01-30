import json
from urllib import request
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "webhooks.json"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False, "endpoints": []}


def post_webhook(event: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    conf = _load_conf()
    if not conf.get("enabled", False):
        return {"status": "disabled"}
    out = []
    for ep in conf.get("endpoints", []):
        if event not in (ep.get("events") or []):
            continue
        url = ep.get("url")
        if not url:
            continue
        body = json.dumps({"event": event, "payload": payload}, ensure_ascii=False).encode("utf-8")
        try:
            req = request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with request.urlopen(req, timeout=5) as resp:
                out.append({"id": ep.get("id"), "status": resp.status})
        except Exception as e:
            out.append({"id": ep.get("id"), "status": "error", "reason": str(e)})
    return {"status": "ok", "results": out}
