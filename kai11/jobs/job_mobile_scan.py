from typing import Dict, Any, List
from ..tools.tool_mobfs import ToolMobfs


class JobMobileScan:
    id = "job.mobile_scan"

    def __init__(self):
        self.tool = ToolMobfs()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
