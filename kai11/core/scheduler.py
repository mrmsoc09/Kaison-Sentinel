import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from .config import OUTPUT_DIR
from .programs import list_programs
from .scope_parser import allowlist_for_program
from .scan_planner import compute_scan_profile, build_scan_pool
from .task_queue import enqueue_task

STATE_PATH = OUTPUT_DIR / "scheduler_state.json"


def _save_state(state: Dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def scheduler_status() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {"status": "never"}
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {"status": "error"}


def build_schedule(scope: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
    profile = compute_scan_profile(scope, options)
    pool = build_scan_pool(profile)
    programs = {p.get("id"): p for p in list_programs()}
    active = []
    skipped = []
    for pid in pool.get("active_programs", []):
        allowlist = allowlist_for_program(pid)
        if not allowlist:
            skipped.append({"program_id": pid, "reason": "no_allowlist"})
            continue
        active.append({"program_id": pid, "allowlist": allowlist, "program": programs.get(pid, {})})
    return {"profile": profile, "pool": pool, "active": active, "skipped": skipped}


def queue_active_plan_tasks(scope: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
    schedule = build_schedule(scope, options)
    queued = []
    for item in schedule.get("active", []):
        task = {
            "mode": "plan",
            "scope": {
                "allowlist": item.get("allowlist") or [],
                "goal": scope.get("goal") or "Autonomous OSINT plan",
                "constraints": scope.get("constraints") or "plan-first",
                "module_kind": scope.get("module_kind") or "osint",
                "budget_tier": scope.get("budget_tier"),
                "stealth": scope.get("stealth"),
            },
        }
        queued.append(enqueue_task(task))
    state = {
        "status": "queued",
        "queued": len(queued),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "schedule": schedule,
    }
    _save_state(state)
    return state
