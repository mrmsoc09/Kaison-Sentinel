from typing import Dict, Any, List
from ..tools.tool_liffy import ToolLiffy


class JobLfiScan:
    id = "job.lfi_scan"

    def __init__(self):
        self.tool = ToolLiffy()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
