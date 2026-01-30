from typing import Dict, Any, List
from ..tools.tool_xsstrike import ToolXsstrike


class JobXssProbe:
    id = "job.xss_probe"

    def __init__(self):
        self.tool = ToolXsstrike()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
