import json
import os
from pathlib import Path
from typing import Dict, Any, List

from ..core.audit import append_audit
from ..core.config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "orchestration.json"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"mode": "hybrid", "osint": {"circles": []}, "vuln": {"circles": []}}


def select_circle(domain: str) -> Dict[str, Any]:
    conf = _load_conf()
    circles: List[Dict[str, Any]] = conf.get(domain, {}).get("circles", [])
    if not circles:
        return {"id": "none", "llm": "none", "governance": "none"}

    forced = os.getenv("KAI_CIRCLE")
    if forced:
        for c in circles:
            if c.get("id") == forced:
                append_audit({"event": "circle_selected", "domain": domain, "circle": c})
                return c

    # round-robin by run id hash could be added later; default to first
    c = circles[0]
    append_audit({"event": "circle_selected", "domain": domain, "circle": c})
    return c


def lang_studio_enabled(domain: str) -> bool:
    conf = _load_conf()
    ls = conf.get(domain, {}).get("lang_studio_cycle", {})
    return bool(ls.get("enabled"))
