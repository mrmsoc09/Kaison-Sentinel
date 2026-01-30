import json
from datetime import datetime
from typing import Dict, Any

from ..core.config import TRACE_DIR

TRACE_DIR.mkdir(parents=True, exist_ok=True)


def record_trace(event: Dict[str, Any]) -> str:
    ts = datetime.utcnow().isoformat()
    event = dict(event)
    event["ts"] = ts
    path = TRACE_DIR / f"trace_{ts.replace(':','')}.json"
    path.write_text(json.dumps(event, ensure_ascii=False, indent=2))
    return str(path)
