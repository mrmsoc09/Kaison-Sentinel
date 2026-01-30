from typing import Dict, Any, List
from ..tools.tool_theharvester import ToolTheharvester


class JobEmailOsint:
    id = "job.email_osint"

    def __init__(self):
        self.tool = ToolTheharvester()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
