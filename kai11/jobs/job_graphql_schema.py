from typing import Dict, Any, List
from ..tools.tool_clairvoyance import ToolClairvoyance


class JobGraphqlSchema:
    id = "job.graphql_schema"

    def __init__(self):
        self.tool = ToolClairvoyance()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
