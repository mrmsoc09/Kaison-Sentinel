from typing import Dict, Any, List
from ..tools.tool_linkfinder import ToolLinkfinder


class JobJsEndpoints:
    id = "job.js_endpoints"

    def __init__(self):
        self.tool = ToolLinkfinder()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
