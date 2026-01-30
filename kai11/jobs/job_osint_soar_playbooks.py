from typing import Dict, Any, List
from ..tools.tool_shuffle import ToolShuffle


class JobOsintSoarPlaybooks:
    id = "job.osint_soar_playbooks"

    def __init__(self):
        self.tool = ToolShuffle()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
