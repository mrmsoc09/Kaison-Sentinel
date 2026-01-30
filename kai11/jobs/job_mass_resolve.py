from typing import Dict, Any, List
from ..tools.tool_massdns import ToolMassdns


class JobMassResolve:
    id = "job.mass_resolve"

    def __init__(self):
        self.tool = ToolMassdns()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
