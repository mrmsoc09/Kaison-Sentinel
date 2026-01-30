from typing import Dict, Any, List
from ..tools.tool_semgrep import ToolSemgrep


class JobSastScan:
    id = "job.sast_scan"

    def __init__(self):
        self.tool = ToolSemgrep()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
