import json
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR
from .redact import redact_text

TRAIN_PATH = OUTPUT_DIR / "training_data.jsonl"


def append_training(event: Dict[str, Any]) -> None:
    # minimal prompt/response; redact sensitive fields
    prompt = f"Summarize artifact type {event.get('type')} for target {event.get('target')}"
    response = redact_text(str(event.get('value')))
    rec = {
        "id": f"train-{event.get('module')}-{event.get('tool')}",
        "prompt": prompt,
        "response": response,
        "type": event.get('type'),
        "target": event.get('target'),
    }
    TRAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRAIN_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
