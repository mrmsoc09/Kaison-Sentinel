from typing import Dict, Any, List
from ..tools.tool_depix import ToolDepix


class JobPixelRecovery:
    id = "job.pixel_recovery"

    def __init__(self):
        self.tool = ToolDepix()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
