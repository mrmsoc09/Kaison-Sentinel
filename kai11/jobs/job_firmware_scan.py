from typing import Dict, Any, List
from ..tools.tool_binwalk import ToolBinwalk


class JobFirmwareScan:
    id = "job.firmware_scan"

    def __init__(self):
        self.tool = ToolBinwalk()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
