from typing import Dict, Any, List
from ..tools.tool_syft import ToolSyft


class JobSbomGeneration:
    id = "job.sbom_generation"

    def __init__(self):
        self.tool = ToolSyft()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
