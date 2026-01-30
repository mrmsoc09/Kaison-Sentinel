from typing import Dict, Any, List
from ..tools.tool_pagodo import ToolPagodo


class JobGoogleDorking:
    id = "job.google_dorking"

    def __init__(self):
        self.tool = ToolPagodo()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
