import json
import time
from typing import Dict, Any, Tuple

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "api_limits.json"
_BUCKETS: Dict[Tuple[str, str], list[float]] = {}


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False}


def check_rate_limit(client_ip: str, route: str) -> Dict[str, Any]:
    conf = _load_conf()
    if not conf.get("enabled", False):
        return {"status": "ok"}
    per_minute = int(conf.get("per_minute", 120))
    per_route = int(conf.get("per_minute_per_route", 60))
    now = time.time()
    key_global = (client_ip, "*")
    key_route = (client_ip, route)

    def _prune(key: Tuple[str, str]) -> list[float]:
        times = _BUCKETS.get(key, [])
        times = [t for t in times if now - t < 60]
        _BUCKETS[key] = times
        return times

    g = _prune(key_global)
    r = _prune(key_route)

    if len(g) >= per_minute or len(r) >= per_route:
        return {"status": "blocked", "reason": "rate_limited"}

    g.append(now)
    r.append(now)
    _BUCKETS[key_global] = g
    _BUCKETS[key_route] = r
    return {"status": "ok"}
