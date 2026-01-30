from typing import Dict, Any, List
from ..tools.tool_trufflehog import ToolTrufflehog


class JobSecretScan:
    id = "job.secret_scan"

    def __init__(self):
        self.tool = ToolTrufflehog()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
