from typing import Dict, Any, List
from ..tools.tool_notify import ToolNotify


class JobNotifications:
    id = "job.notifications"

    def __init__(self):
        self.tool = ToolNotify()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
