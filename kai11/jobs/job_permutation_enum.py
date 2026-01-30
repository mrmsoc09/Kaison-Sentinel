from typing import Dict, Any, List
from ..tools.tool_altdns import ToolAltdns


class JobPermutationEnum:
    id = "job.permutation_enum"

    def __init__(self):
        self.tool = ToolAltdns()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
