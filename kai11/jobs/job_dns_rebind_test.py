from typing import Dict, Any, List
from ..tools.tool_httprebind import ToolHttprebind


class JobDnsRebindTest:
    id = "job.dns_rebind_test"

    def __init__(self):
        self.tool = ToolHttprebind()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
