from typing import Dict, Any, List
from ..tools.tool_qsreplace import ToolQsreplace


class JobQueryReplace:
    id = "job.query_replace"

    def __init__(self):
        self.tool = ToolQsreplace()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
