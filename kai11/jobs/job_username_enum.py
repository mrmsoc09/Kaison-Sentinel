from typing import Dict, Any, List
from ..tools.tool_maigret import ToolMaigret


class JobUsernameEnum:
    id = "job.username_enum"

    def __init__(self):
        self.tool = ToolMaigret()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
