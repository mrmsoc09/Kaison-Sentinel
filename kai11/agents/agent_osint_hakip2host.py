from typing import Dict, Any, List
from ..jobs.job_ip_to_host import JobIpToHost
from ..core.audit import append_audit


class AgentOsintHakip2host:
    id = "agent.osint_hakip2host"

    def __init__(self):
        self.job = JobIpToHost()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id})
        return result
