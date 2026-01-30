from typing import Dict, Any, List
from ..tools.tool_hakrawler import ToolHakrawler


class JobCrawlUrls:
    id = "job.crawl_urls"

    def __init__(self):
        self.tool = ToolHakrawler()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
