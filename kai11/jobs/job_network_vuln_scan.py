from typing import Dict, Any, List
from ..tools.tool_nmap_vuln import ToolNmapVuln


class JobNetworkVulnScan:
    id = "job.network_vuln_scan"

    def __init__(self):
        self.tool = ToolNmapVuln()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
