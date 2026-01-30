from typing import Dict, Any, List
from ..tools.tool_sn0int import ToolSn0int


class JobOsintCollection:
    id = "job.osint_collection"

    def __init__(self):
        self.tool = ToolSn0int()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
