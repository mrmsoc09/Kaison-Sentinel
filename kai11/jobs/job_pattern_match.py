from typing import Dict, Any, List
from ..tools.tool_gf import ToolGf


class JobPatternMatch:
    id = "job.pattern_match"

    def __init__(self):
        self.tool = ToolGf()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
