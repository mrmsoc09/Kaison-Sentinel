from typing import Dict, Any, List
from ..tools.tool_reconng import ToolReconng


class JobReconFramework:
    id = "job.recon_framework"

    def __init__(self):
        self.tool = ToolReconng()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
