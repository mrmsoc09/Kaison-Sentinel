from typing import Dict, Any, List
from ..tools.tool_pastehunter import ToolPastehunter


class JobPasteMonitor:
    id = "job.paste_monitor"

    def __init__(self):
        self.tool = ToolPastehunter()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
