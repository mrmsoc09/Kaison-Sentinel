from typing import Dict, Any, List
from ..tools.tool_inql import ToolInql


class JobGraphqlTest:
    id = "job.graphql_test"

    def __init__(self):
        self.tool = ToolInql()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
