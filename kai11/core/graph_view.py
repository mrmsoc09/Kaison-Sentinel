import json
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR


def load_latest_graph() -> Dict[str, Any]:
    files = sorted(OUTPUT_DIR.glob("*_graph.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return {"nodes": [], "edges": []}
    return json.loads(files[0].read_text())
