from typing import Dict, Any, List
from ..tools.tool_wazuh import ToolWazuh


class JobSecurityEventIngest:
    id = "job.security_event_ingest"

    def __init__(self):
        self.tool = ToolWazuh()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
