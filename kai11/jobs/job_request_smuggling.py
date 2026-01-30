from typing import Dict, Any, List
from ..tools.tool_smuggler import ToolSmuggler


class JobRequestSmuggling:
    id = "job.request_smuggling"

    def __init__(self):
        self.tool = ToolSmuggler()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
