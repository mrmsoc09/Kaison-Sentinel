from typing import Dict, Any, List
from ..tools.tool_amass import ToolAmass


class JobEnumerateSubdomains:
    id = "job.enumerate_subdomains"

    def __init__(self):
        self.tool = ToolAmass()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
