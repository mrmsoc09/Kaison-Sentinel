from typing import Dict, Any, List
from ..tools.tool_gau import ToolGau


class JobArchiveUrls:
    id = "job.archive_urls"

    def __init__(self):
        self.tool = ToolGau()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
