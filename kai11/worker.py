import json
import time

from .core.task_queue import fetch_next_task, mark_job
from .core.program_sync import sync_program_scopes, maybe_auto_sync
from .core.scan_engine import run_execute, run_plan


def run_worker(poll_interval: int = 3) -> None:
    while True:
        task = fetch_next_task()
        if not task:
            maybe_auto_sync()
            time.sleep(poll_interval)
            continue
        job_id = task.get("job_id", "job-unknown")
        mark_job(job_id, "running")
        try:
            mode = task.get("mode", "execute")
            if mode == "program_sync":
                result = sync_program_scopes(force=bool(task.get("force")))
            else:
                scope = task.get("scope") or {}
                if mode == "plan":
                    result = run_plan(scope)
                else:
                    result = run_execute(scope, approved=task.get("approve", False), mitigation_tier=task.get("tier", "standard"))
            mark_job(job_id, "completed", {"result": result})
        except Exception as e:
            mark_job(job_id, "error", {"error": str(e)})


if __name__ == "__main__":
    run_worker()
