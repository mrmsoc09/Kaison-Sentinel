from typing import Dict, Any, List
from ..tools.tool_assetfinder import ToolAssetfinder


class JobFindAssets:
    id = "job.find_assets"

    def __init__(self):
        self.tool = ToolAssetfinder()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
