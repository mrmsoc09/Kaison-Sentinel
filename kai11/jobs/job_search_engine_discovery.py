from typing import Dict, Any, List
from ..tools.tool_uncover import ToolUncover


class JobSearchEngineDiscovery:
    id = "job.search_engine_discovery"

    def __init__(self):
        self.tool = ToolUncover()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
