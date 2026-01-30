from typing import Dict, Any, List
from ..tools.tool_graphw00f import ToolGraphw00f


class JobGraphqlFingerprint:
    id = "job.graphql_fingerprint"

    def __init__(self):
        self.tool = ToolGraphw00f()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
