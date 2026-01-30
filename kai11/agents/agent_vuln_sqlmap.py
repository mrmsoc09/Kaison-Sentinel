from typing import Dict, Any, List
from ..jobs.job_sql_injection_probe import JobSqlInjectionProbe
from ..core.audit import append_audit


class AgentVulnSqlmap:
    id = "agent.vuln_sqlmap"

    def __init__(self):
        self.job = JobSqlInjectionProbe()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id})
        return result
