from typing import Dict, Any, List
from ..tools.tool_cariddi import ToolCariddi


class JobCrawlAndSecrets:
    id = "job.crawl_and_secrets"

    def __init__(self):
        self.tool = ToolCariddi()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
