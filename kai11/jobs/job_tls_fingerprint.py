from typing import Dict, Any, List
from ..tools.tool_tlsx import ToolTlsx


class JobTlsFingerprint:
    id = "job.tls_fingerprint"

    def __init__(self):
        self.tool = ToolTlsx()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
