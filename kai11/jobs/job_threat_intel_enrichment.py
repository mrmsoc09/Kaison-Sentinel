from typing import Dict, Any, List
from ..tools.tool_intelowl import ToolIntelowl


class JobThreatIntelEnrichment:
    id = "job.threat_intel_enrichment"

    def __init__(self):
        self.tool = ToolIntelowl()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
