from typing import Dict, Any, List
from ..tools.tool_fdsploit import ToolFdsploit


class JobPathTraversalFuzz:
    id = "job.path_traversal_fuzz"

    def __init__(self):
        self.tool = ToolFdsploit()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
