from typing import Dict, Any, List
from ..tools.tool_secretfinder import ToolSecretfinder


class JobJsSecretScan:
    id = "job.js_secret_scan"

    def __init__(self):
        self.tool = ToolSecretfinder()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
