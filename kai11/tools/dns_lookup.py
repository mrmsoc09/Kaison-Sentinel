import socket
from typing import Dict, Any


class DNSLookupTool:
    id = "tool.dns_lookup"

    def run(self, target: str) -> Dict[str, Any]:
        try:
            host, aliases, ips = socket.gethostbyname_ex(target)
            return {"target": target, "host": host, "aliases": aliases, "ips": ips}
        except Exception as e:
            return {"target": target, "error": str(e), "ips": []}
