from typing import Dict, Any, List
from ..tools.tool_kiterunner import ToolKiterunner


class JobApiDiscovery:
    id = "job.api_discovery"

    def __init__(self):
        self.tool = ToolKiterunner()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
