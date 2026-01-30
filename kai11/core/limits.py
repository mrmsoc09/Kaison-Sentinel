import os
import time
from threading import Lock
from typing import Dict, Any

_last_call = 0.0
_lock = Lock()


def rate_limit(options: Dict[str, Any] | None = None, tool_id: str | None = None) -> None:
    interval_ms = int(os.getenv("KAI_MIN_INTERVAL_MS", "0"))
    if options:
        interval_ms = int(options.get("rate_limits", {}).get("global_min_interval_ms", interval_ms))
        per_tool = options.get("rate_limits", {}).get("per_tool", {})
        if tool_id and tool_id in per_tool:
            interval_ms = int(per_tool.get(tool_id, interval_ms))

    if interval_ms <= 0:
        return
    global _last_call
    with _lock:
        now = time.time()
        elapsed = (now - _last_call) * 1000
        if elapsed < interval_ms:
            time.sleep((interval_ms - elapsed) / 1000)
        _last_call = time.time()
