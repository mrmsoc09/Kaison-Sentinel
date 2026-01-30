from typing import Dict, Any, List
from ..tools.tool_misp import ToolMisp


class JobThreatIntelIngest:
    id = "job.threat_intel_ingest"

    def __init__(self):
        self.tool = ToolMisp()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
