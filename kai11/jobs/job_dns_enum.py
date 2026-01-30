from typing import Dict, Any, List
from ..tools.tool_dnsenum import ToolDnsenum


class JobDnsEnum:
    id = "job.dns_enum"

    def __init__(self):
        self.tool = ToolDnsenum()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
