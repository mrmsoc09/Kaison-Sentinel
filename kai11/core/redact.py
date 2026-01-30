import json
import re
from pathlib import Path
from typing import List, Dict

from .config import BUILD_ROOT, LOGS_DIR

CONF = BUILD_ROOT / "config" / "governance.json"

_stats: Dict[str, int] = {"total": 0, "password": 0, "api_key": 0, "token": 0, "secret": 0, "bearer": 0}


def _load_patterns() -> List[str]:
    try:
        data = json.loads(CONF.read_text())
        return data.get("redact_patterns", [])
    except Exception:
        return []


def _count(kind: str, before: str, after: str) -> None:
    if before != after:
        _stats["total"] += 1
        _stats[kind] = _stats.get(kind, 0) + 1


def redact_text(text: str) -> str:
    red = text
    # Redact common key=value secrets first
    before = red
    red = re.sub(r"(password=)(\S+)", r"\1[REDACTED]", red, flags=re.IGNORECASE)
    _count("password", before, red)

    before = red
    red = re.sub(r"(api_key=)(\S+)", r"\1[REDACTED]", red, flags=re.IGNORECASE)
    _count("api_key", before, red)

    before = red
    red = re.sub(r"(token=)(\S+)", r"\1[REDACTED]", red, flags=re.IGNORECASE)
    _count("token", before, red)

    before = red
    red = re.sub(r"(secret=)(\S+)", r"\1[REDACTED]", red, flags=re.IGNORECASE)
    _count("secret", before, red)

    before = red
    red = re.sub(r"(authorization:\s*bearer\s+)(\S+)", r"\1[REDACTED]", red, flags=re.IGNORECASE)
    _count("bearer", before, red)

    for p in _load_patterns():
        try:
            red = re.sub(re.escape(p), "[REDACTED]", red)
        except re.error:
            red = red.replace(p, "[REDACTED]")
    return red


def redaction_summary() -> Dict[str, int]:
    return dict(_stats)


def write_redaction_summary(run_id: str) -> str:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    path = LOGS_DIR / f"{run_id}_redaction_summary.json"
    path.write_text(json.dumps(redaction_summary(), ensure_ascii=False, indent=2))
    return str(path)
