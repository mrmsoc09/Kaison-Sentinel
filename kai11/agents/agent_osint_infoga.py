from typing import Dict, Any, List
from ..jobs.job_email_enum import JobEmailEnum
from ..core.audit import append_audit


class AgentOsintInfoga:
    id = "agent.osint_infoga"

    def __init__(self):
        self.job = JobEmailEnum()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id})
        return result
