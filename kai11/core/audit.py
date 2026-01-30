import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from .config import LOGS_DIR
from .redact import redact_text

LOGS_DIR.mkdir(parents=True, exist_ok=True)


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_audit(event: Dict[str, Any]) -> str:
    path = LOGS_DIR / "audit.jsonl"
    line = {"ts": _ts(), **event}
    # redact string fields
    for k, v in list(line.items()):
        if isinstance(v, str):
            line[k] = redact_text(v)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return str(path)
