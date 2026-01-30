from typing import Dict, Any, List
from ..tools.tool_sqlmap import ToolSqlmap


class JobSqlInjectionProbe:
    id = "job.sql_injection_probe"

    def __init__(self):
        self.tool = ToolSqlmap()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
