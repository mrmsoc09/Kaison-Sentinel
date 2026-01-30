from typing import Dict, Any, List
from ..tools.tool_subjack import ToolSubjack


class JobSubdomainTakeoverCheck:
    id = "job.subdomain_takeover_check"

    def __init__(self):
        self.tool = ToolSubjack()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
