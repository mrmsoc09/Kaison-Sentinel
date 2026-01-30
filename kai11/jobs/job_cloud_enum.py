from typing import Dict, Any, List
from ..tools.tool_cloudbrute import ToolCloudbrute


class JobCloudEnum:
    id = "job.cloud_enum"

    def __init__(self):
        self.tool = ToolCloudbrute()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
