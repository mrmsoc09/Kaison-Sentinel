from typing import Dict, Any, List
from ..tools.tool_fingerprintx import ToolFingerprintx


class JobServiceFingerprint:
    id = "job.service_fingerprint"

    def __init__(self):
        self.tool = ToolFingerprintx()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
