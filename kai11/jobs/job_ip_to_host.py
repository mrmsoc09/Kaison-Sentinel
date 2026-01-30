from typing import Dict, Any, List
from ..tools.tool_hakip2host import ToolHakip2host


class JobIpToHost:
    id = "job.ip_to_host"

    def __init__(self):
        self.tool = ToolHakip2host()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
