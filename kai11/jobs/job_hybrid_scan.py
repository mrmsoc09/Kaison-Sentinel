from typing import Dict, Any, List
from ..tools.tool_scancannon import ToolScancannon


class JobHybridScan:
    id = "job.hybrid_scan"

    def __init__(self):
        self.tool = ToolScancannon()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
