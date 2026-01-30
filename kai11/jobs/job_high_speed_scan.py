from typing import Dict, Any, List
from ..tools.tool_masscan import ToolMasscan


class JobHighSpeedScan:
    id = "job.high_speed_scan"

    def __init__(self):
        self.tool = ToolMasscan()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
