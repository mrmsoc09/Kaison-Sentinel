from typing import Dict, Any, List
from ..tools.tool_h8mail import ToolH8mail


class JobBreachSearch:
    id = "job.breach_search"

    def __init__(self):
        self.tool = ToolH8mail()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
