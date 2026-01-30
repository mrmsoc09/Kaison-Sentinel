import json
import time
from pathlib import Path
from typing import Dict, Any, List

from .config import OUTPUT_DIR

QUEUE_DIR = OUTPUT_DIR / "queue"
QUEUE_FILE = QUEUE_DIR / "queue.jsonl"
STATE_FILE = QUEUE_DIR / "queue_state.json"


def _load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def _save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def enqueue_task(task: Dict[str, Any]) -> Dict[str, Any]:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    job_id = task.get("job_id") or f"job-{int(time.time())}"
    task["job_id"] = job_id
    with QUEUE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(task, ensure_ascii=False) + "\n")
    state = _load_state()
    state[job_id] = {"status": "queued", "created_at": time.time()}
    _save_state(state)
    return {"status": "queued", "job_id": job_id}


def list_jobs() -> List[Dict[str, Any]]:
    state = _load_state()
    out = []
    for job_id, meta in state.items():
        item = {"job_id": job_id}
        item.update(meta)
        out.append(item)
    return sorted(out, key=lambda x: x.get("created_at", 0), reverse=True)


def mark_job(job_id: str, status: str, detail: Dict[str, Any] | None = None) -> None:
    state = _load_state()
    record = state.get(job_id, {"created_at": time.time()})
    record["status"] = status
    record["updated_at"] = time.time()
    if detail:
        record["detail"] = detail
    state[job_id] = record
    _save_state(state)


def fetch_next_task() -> Dict[str, Any] | None:
    if not QUEUE_FILE.exists():
        return None
    lines = QUEUE_FILE.read_text().splitlines()
    if not lines:
        return None
    task = json.loads(lines[0])
    # rewrite queue without first line
    QUEUE_FILE.write_text("\n".join(lines[1:]) + ("\n" if len(lines) > 1 else ""))
    return task
