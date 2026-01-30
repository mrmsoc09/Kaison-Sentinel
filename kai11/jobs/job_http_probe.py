from typing import Dict, Any, List
from ..tools.tool_httpx import ToolHttpx


class JobHttpProbe:
    id = "job.http_probe"

    def __init__(self):
        self.tool = ToolHttpx()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
