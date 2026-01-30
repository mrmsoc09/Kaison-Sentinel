from typing import Dict, Any, List
from ..tools.tool_cut_cdn import ToolCutCdn


class JobCdnIpFilter:
    id = "job.cdn_ip_filter"

    def __init__(self):
        self.tool = ToolCutCdn()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
