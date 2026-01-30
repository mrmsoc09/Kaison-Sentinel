from typing import Dict, Any, List
from ..tools.tool_paramspider import ToolParamspider


class JobParamDiscovery:
    id = "job.param_discovery"

    def __init__(self):
        self.tool = ToolParamspider()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
