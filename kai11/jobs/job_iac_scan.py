from typing import Dict, Any, List
from ..tools.tool_tfsec import ToolTfsec


class JobIacScan:
    id = "job.iac_scan"

    def __init__(self):
        self.tool = ToolTfsec()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
