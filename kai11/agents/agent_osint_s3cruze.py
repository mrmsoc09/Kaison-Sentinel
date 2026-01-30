from typing import Dict, Any, List
from ..jobs.job_s3_bucket_enum import JobS3BucketEnum
from ..core.audit import append_audit


class AgentOsintS3cruze:
    id = "agent.osint_s3cruze"

    def __init__(self):
        self.job = JobS3BucketEnum()

    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_start", "agent": self.id, "circle": circle})
        result = self.job.run(targets, options=circle.get("options"))
        append_audit({"event": "agent_done", "agent": self.id})
        return result
