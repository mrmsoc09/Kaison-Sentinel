from typing import Dict, Any, List
from ..tools.tool_uro import ToolUro


class JobUrlDedupe:
    id = "job.url_dedupe"

    def __init__(self):
        self.tool = ToolUro()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
