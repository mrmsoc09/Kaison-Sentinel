from typing import Dict, Any, List
from ..tools.tool_pdfid import ToolPdfid


class JobPdfAnalysis:
    id = "job.pdf_analysis"

    def __init__(self):
        self.tool = ToolPdfid()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
