from typing import Dict, Any, List
from ..tools.tool_sandmap import ToolSandmap


class JobProfiledScan:
    id = "job.profiled_scan"

    def __init__(self):
        self.tool = ToolSandmap()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
