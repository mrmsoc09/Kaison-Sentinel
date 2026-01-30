from typing import Dict, Any, List
from ..tools.tool_nuclei import ToolNuclei


class JobTemplateScan:
    id = "job.template_scan"

    def __init__(self):
        self.tool = ToolNuclei()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
