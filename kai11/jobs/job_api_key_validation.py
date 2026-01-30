from typing import Dict, Any, List
from ..tools.tool_keyhacks import ToolKeyhacks


class JobApiKeyValidation:
    id = "job.api_key_validation"

    def __init__(self):
        self.tool = ToolKeyhacks()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
