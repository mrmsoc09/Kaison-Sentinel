from typing import Dict, Any, List
from ..tools.tool_searxng import ToolSearxng


class JobMetasearch:
    id = "job.metasearch"

    def __init__(self):
        self.tool = ToolSearxng()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
