from typing import Dict, Any, List
from ..tools.tool_retirejs import ToolRetirejs


class JobJsVulnFingerprint:
    id = "job.js_vuln_fingerprint"

    def __init__(self):
        self.tool = ToolRetirejs()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
