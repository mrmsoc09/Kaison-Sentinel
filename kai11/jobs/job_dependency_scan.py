from typing import Dict, Any, List
from ..tools.tool_osv_scanner import ToolOsvScanner


class JobDependencyScan:
    id = "job.dependency_scan"

    def __init__(self):
        self.tool = ToolOsvScanner()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
