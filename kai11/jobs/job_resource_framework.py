from typing import Dict, Any, List
from ..tools.tool_osintframework import ToolOsintframework


class JobResourceFramework:
    id = "job.resource_framework"

    def __init__(self):
        self.tool = ToolOsintframework()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
