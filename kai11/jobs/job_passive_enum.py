from typing import Dict, Any, List
from ..tools.tool_chaos_client import ToolChaosClient


class JobPassiveEnum:
    id = "job.passive_enum"

    def __init__(self):
        self.tool = ToolChaosClient()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
