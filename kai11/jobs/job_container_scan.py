from typing import Dict, Any, List
from ..tools.tool_trivy import ToolTrivy


class JobContainerScan:
    id = "job.container_scan"

    def __init__(self):
        self.tool = ToolTrivy()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
