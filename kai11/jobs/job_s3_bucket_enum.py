from typing import Dict, Any, List
from ..tools.tool_s3cario import ToolS3cario


class JobS3BucketEnum:
    id = "job.s3_bucket_enum"

    def __init__(self):
        self.tool = ToolS3cario()

    def run(self, targets: List[str], **kwargs) -> Dict[str, Any]:
        results = []
        for t in targets:
            results.append(self.tool.run(t, options=kwargs.get("options")))
        return {"results": results}
