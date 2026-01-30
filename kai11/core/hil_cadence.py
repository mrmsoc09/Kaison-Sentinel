from datetime import datetime, timedelta
from typing import Dict, Any, Optional


def _parse_run_time(run_id: str) -> Optional[datetime]:
    # run-YYYYMMDD-HHMMSS
    try:
        parts = run_id.split("-")
        if len(parts) < 3:
            return None
        dt = datetime.strptime(parts[1] + parts[2], "%Y%m%d%H%M%S")
        return dt
    except Exception:
        return None


def _parse_iso(ts: str | None) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def compute_hil_cadence(run_id: str, scope: Dict[str, Any], interval_minutes: int = 120) -> Dict[str, Any]:
    now = datetime.utcnow()
    run_time = _parse_run_time(run_id)
    last_confirmed = _parse_iso(scope.get("report_hil_confirmed_at")) or _parse_iso(scope.get("validation_confirmed_at")) or _parse_iso(scope.get("hil_confirmed_at"))
    if last_confirmed is None:
        last_confirmed = run_time
    next_due = (last_confirmed + timedelta(minutes=interval_minutes)) if last_confirmed else None
    overdue = bool(next_due and now > next_due and not scope.get("report_hil_confirmed"))
    status = "ok" if scope.get("report_hil_confirmed") else ("overdue" if overdue else "pending")
    return {
        "interval_minutes": interval_minutes,
        "last_confirmed_at": last_confirmed.isoformat() if last_confirmed else "",
        "next_due_at": next_due.isoformat() if next_due else "",
        "status": status,
    }
