from typing import Dict, Any, List
from ..tools.tool_dnsx import ToolDnsx


class JobResolveDns:
    id = "job.resolve_dns"

    def __init__(self):
        self.tool = ToolDnsx()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
