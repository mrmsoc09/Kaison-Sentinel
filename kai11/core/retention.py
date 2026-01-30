import json
import time
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR, BUILD_ROOT

CONF = BUILD_ROOT / "config" / "retention.json"
ARCHIVE_DIR = OUTPUT_DIR / "archive"


def _load_conf() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False}


def _apply_dir(dir_path: Path, days: int, action: str) -> int:
    if days <= 0:
        return 0
    cutoff = time.time() - (days * 86400)
    moved = 0
    for p in dir_path.glob("*"):
        try:
            if p.stat().st_mtime > cutoff:
                continue
            if action == "archive":
                ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
                target = ARCHIVE_DIR / p.name
                p.rename(target)
            elif action == "delete":
                if p.is_dir():
                    for c in p.glob("**/*"):
                        if c.is_file():
                            c.unlink(missing_ok=True)
                    p.rmdir()
                else:
                    p.unlink(missing_ok=True)
            moved += 1
        except Exception:
            continue
    return moved


def apply_retention() -> Dict[str, Any]:
    conf = _load_conf()
    if not conf.get("enabled", False):
        return {"status": "disabled"}
    action = conf.get("action", "archive")
    days = conf.get("days", {})
    summary = {}
    for key, dir_name in [
        ("runs", "runs"),
        ("reports", "reports"),
        ("evidence", "evidence"),
        ("logs", "logs"),
        ("alerts", "alerts"),
        ("emails", "emails"),
    ]:
        summary[key] = _apply_dir(OUTPUT_DIR / dir_name, int(days.get(key, 0)), action)
    return {"status": "ok", "action": action, "moved": summary}
