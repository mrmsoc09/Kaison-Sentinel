from typing import Dict, Any, List
from ..tools.tool_sslscan import ToolSslscan


class JobTlsScan:
    id = "job.tls_scan"

    def __init__(self):
        self.tool = ToolSslscan()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
