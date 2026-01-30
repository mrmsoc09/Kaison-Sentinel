from typing import Dict, Any, List
from ..tools.tool_jsmon import ToolJsmon


class JobJsChangeMonitor:
    id = "job.js_change_monitor"

    def __init__(self):
        self.tool = ToolJsmon()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
