from typing import Dict, Any, List
from ..tools.tool_nikto import ToolNikto


class JobWebServerScan:
    id = "job.web_server_scan"

    def __init__(self):
        self.tool = ToolNikto()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
