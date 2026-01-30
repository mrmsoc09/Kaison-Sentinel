from typing import Dict, Any, List
from ..tools.tool_twint import ToolTwint


class JobTwitterOsint:
    id = "job.twitter_osint"

    def __init__(self):
        self.tool = ToolTwint()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
