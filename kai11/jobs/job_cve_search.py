from typing import Dict, Any, List
from ..tools.tool_cvemap import ToolCvemap


class JobCveSearch:
    id = "job.cve_search"

    def __init__(self):
        self.tool = ToolCvemap()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
