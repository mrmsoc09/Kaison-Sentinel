import json
import os
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Any, List
from urllib.request import Request, urlopen

from .config import BUILD_ROOT, OUTPUT_DIR
from .programs import list_programs
from .options import get_options

CACHE_DIR = BUILD_ROOT / "data" / "programs" / "scopes"
STATE_PATH = OUTPUT_DIR / "program_sync.json"
OPPORTUNITY_SNAPSHOT = OUTPUT_DIR / "program_opportunities.json"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: List[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self._parts.append(data.strip())

    def text(self) -> str:
        joined = " ".join(self._parts)
        joined = re.sub(r"\s+", " ", joined)
        return joined.strip()


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def _fetch(url: str, timeout: int = 20) -> Dict[str, Any]:
    headers = {
        "User-Agent": "KaisonSentinel/1.0 (+https://kaisonai.com) program-sync",
        "Accept": "text/html,application/xhtml+xml",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
            content_type = resp.headers.get("Content-Type", "")
        return {
            "ok": True,
            "status": status,
            "content_type": content_type,
            "body": raw,
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "status": None, "content_type": "", "body": b""}


def _write_text(path: Path, html: bytes) -> None:
    parser = _TextExtractor()
    try:
        parser.feed(html.decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return
    text = parser.text()
    path.write_text(text + "\n", encoding="utf-8")


def _save_state(state: Dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def program_sync_status() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {"status": "never", "last_sync": None, "count": 0}
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {"status": "error", "last_sync": None, "count": 0}


def snapshot_opportunities(programs: List[Dict[str, Any]]) -> Dict[str, Any]:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(programs),
        "programs": programs,
    }
    OPPORTUNITY_SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    OPPORTUNITY_SNAPSHOT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return {"path": str(OPPORTUNITY_SNAPSHOT), "count": len(programs)}


def sync_program_scopes(
    allow_network: bool | None = None,
    sleep_seconds: float = 1.5,
    force: bool = False,
) -> Dict[str, Any]:
    options = get_options("all")
    cfg = options.get("program_sync", {})
    enabled = bool(cfg.get("enabled", False))

    if not enabled and not force:
        return {"status": "disabled", "reason": "program_sync_disabled"}

    network_allowed = allow_network
    if network_allowed is None:
        network_allowed = os.getenv("KAI_ALLOW_NETWORK") == "1"
    if not network_allowed:
        state = {
            "status": "blocked",
            "reason": "network_disabled",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "count": 0,
        }
        _save_state(state)
        return state

    programs = list_programs()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    errors = 0
    for program in programs:
        pid = _safe_name(program.get("id") or program.get("name") or "unknown")
        scope_url = program.get("scope_url") or ""
        policy_url = program.get("policy_url") or ""
        if not scope_url and not policy_url:
            continue
        dest = CACHE_DIR / pid
        dest.mkdir(parents=True, exist_ok=True)
        meta = {
            "id": program.get("id"),
            "name": program.get("name"),
            "platform": program.get("platform"),
            "scope_url": scope_url,
            "policy_url": policy_url,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "scope": {},
            "policy": {},
        }

        if scope_url:
            res = _fetch(scope_url)
            meta["scope"] = {k: v for k, v in res.items() if k != "body"}
            if res.get("ok") and res.get("body"):
                (dest / "scope.html").write_bytes(res["body"])
                _write_text(dest / "scope.txt", res["body"])
            else:
                errors += 1
            time.sleep(sleep_seconds)

        if policy_url:
            res = _fetch(policy_url)
            meta["policy"] = {k: v for k, v in res.items() if k != "body"}
            if res.get("ok") and res.get("body"):
                (dest / "policy.html").write_bytes(res["body"])
                _write_text(dest / "policy.txt", res["body"])
            else:
                errors += 1
            time.sleep(sleep_seconds)

        (dest / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    opp = snapshot_opportunities(programs)
    state = {
        "status": "ok",
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "count": len(programs),
        "errors": errors,
        "opportunities": opp,
    }
    _save_state(state)
    return state


def maybe_auto_sync() -> Dict[str, Any] | None:
    options = get_options("all")
    cfg = options.get("program_sync", {})
    if not cfg.get("enabled"):
        return None
    if not cfg.get("auto_trigger", False):
        return None
    interval_hours = float(cfg.get("interval_hours", 24))
    state = program_sync_status()
    last = state.get("last_sync")
    if last:
        try:
            last_ts = datetime.fromisoformat(last).timestamp()
        except Exception:
            last_ts = 0.0
    else:
        last_ts = 0.0
    due = (time.time() - last_ts) >= interval_hours * 3600
    if not due:
        return None
    return sync_program_scopes(allow_network=None, sleep_seconds=float(cfg.get("sleep_seconds", 1.5)))
