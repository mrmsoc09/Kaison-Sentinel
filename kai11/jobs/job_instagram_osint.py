from typing import Dict, Any, List
from ..tools.tool_osintgram import ToolOsintgram


class JobInstagramOsint:
    id = "job.instagram_osint"

    def __init__(self):
        self.tool = ToolOsintgram()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
