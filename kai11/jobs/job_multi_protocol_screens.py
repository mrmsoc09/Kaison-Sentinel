from typing import Dict, Any, List
from ..tools.tool_scrying import ToolScrying


class JobMultiProtocolScreens:
    id = "job.multi_protocol_screens"

    def __init__(self):
        self.tool = ToolScrying()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
