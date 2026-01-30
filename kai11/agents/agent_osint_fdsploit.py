from typing import Dict, Any, List
from ..jobs.job_path_traversal_fuzz import JobPathTraversalFuzz
from ..core.audit import append_audit


class AgentOsintFdsploit:
    id = "agent.osint_fdsploit"

    def __init__(self):
        self.job = JobPathTraversalFuzz()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id})
        return result
