from typing import Dict, Any, List
from ..tools.tool_unfurl import ToolUnfurl


class JobUrlParse:
    id = "job.url_parse"

    def __init__(self):
        self.tool = ToolUnfurl()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
