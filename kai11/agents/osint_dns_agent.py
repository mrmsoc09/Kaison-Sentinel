from typing import Dict, Any, List
from ..jobs.run_dns_lookup import RunDNSLookupJob
from ..core.audit import append_audit


class OsintDNSAgent:
    id = "agent.osint_dns"

    def __init__(self):
        self.job = RunDNSLookupJob()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id, "assets": len(result.get("assets", []))})
        return result
