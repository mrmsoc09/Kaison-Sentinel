from typing import Dict, Any, List
from ..tools.dns_lookup import DNSLookupTool


class RunDNSLookupJob:
    id = "job.dns_lookup"

    def __init__(self):
        self.tool = DNSLookupTool()

    def run(self, targets: List[str]) -> Dict[str, Any]:
        results = []
        assets: List[str] = []
        for t in targets:
            res = self.tool.run(t)
            results.append(res)
            for ip in res.get("ips", []):
                assets.append(ip)
        return {"results": results, "assets": sorted(set(assets))}
