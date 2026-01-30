from typing import Dict, Any, List
from ..tools.tool_spiderfoot import ToolSpiderfoot


class JobOsintAutomation:
    id = "job.osint_automation"

    def __init__(self):
        self.tool = ToolSpiderfoot()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
