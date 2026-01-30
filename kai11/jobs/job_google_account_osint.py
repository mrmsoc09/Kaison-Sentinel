from typing import Dict, Any, List
from ..tools.tool_ghunt import ToolGhunt


class JobGoogleAccountOsint:
    id = "job.google_account_osint"

    def __init__(self):
        self.tool = ToolGhunt()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
