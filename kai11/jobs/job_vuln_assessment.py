from typing import Dict, Any, List
from ..tools.tool_gvm import ToolGvm


class JobVulnAssessment:
    id = "job.vuln_assessment"

    def __init__(self):
        self.tool = ToolGvm()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
