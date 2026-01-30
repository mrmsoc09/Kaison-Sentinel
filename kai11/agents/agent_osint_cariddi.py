from typing import Dict, Any, List
from ..jobs.job_crawl_and_secrets import JobCrawlAndSecrets
from ..core.audit import append_audit


class AgentOsintCariddi:
    id = "agent.osint_cariddi"

    def __init__(self):
        self.job = JobCrawlAndSecrets()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id})
        return result
