from typing import Dict, Any, List
from ..tools.tool_zmap import ToolZmap


class JobInternetScan:
    id = "job.internet_scan"

    def __init__(self):
        self.tool = ToolZmap()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
