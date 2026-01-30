import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR

KNOW_PATH = OUTPUT_DIR / "knowledge_store.jsonl"


def append_knowledge(event: Dict[str, Any]) -> None:
    payload = dict(event)
    payload.setdefault("ts", datetime.utcnow().isoformat())
    with KNOW_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
