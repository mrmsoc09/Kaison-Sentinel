from typing import Dict, Any, List
from ..tools.tool_aquatone import ToolAquatone


class JobWebScreenshots:
    id = "job.web_screenshots"

    def __init__(self):
        self.tool = ToolAquatone()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
