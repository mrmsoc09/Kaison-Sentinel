from typing import Dict, Any, List
from ..tools.tool_zap_cli import ToolZapCli


class JobWebDynamicScan:
    id = "job.web_dynamic_scan"

    def __init__(self):
        self.tool = ToolZapCli()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
