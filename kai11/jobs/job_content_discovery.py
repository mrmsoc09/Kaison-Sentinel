from typing import Dict, Any, List
from ..tools.tool_ffuf import ToolFfuf


class JobContentDiscovery:
    id = "job.content_discovery"

    def __init__(self):
        self.tool = ToolFfuf()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
