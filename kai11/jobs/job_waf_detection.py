from typing import Dict, Any, List
from ..tools.tool_wafw00f import ToolWafw00f


class JobWafDetection:
    id = "job.waf_detection"

    def __init__(self):
        self.tool = ToolWafw00f()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
