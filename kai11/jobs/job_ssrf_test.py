from typing import Dict, Any, List
from ..tools.tool_ssrfmap import ToolSsrfmap


class JobSsrfTest:
    id = "job.ssrf_test"

    def __init__(self):
        self.tool = ToolSsrfmap()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
