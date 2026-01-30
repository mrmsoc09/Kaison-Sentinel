from typing import Dict, Any, List
from ..tools.tool_metagoofil import ToolMetagoofil


class JobMetadataExtract:
    id = "job.metadata_extract"

    def __init__(self):
        self.tool = ToolMetagoofil()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
