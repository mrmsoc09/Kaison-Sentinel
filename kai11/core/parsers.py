import json
import re
from typing import Dict, Any, List


def parse_lines(stdout: str) -> List[str]:
    lines = [l.strip() for l in stdout.splitlines() if l.strip()]
    return lines


def parse_json(stdout: str) -> Any:
    try:
        return json.loads(stdout)
    except Exception:
        return None


def parse_jsonl(stdout: str) -> List[Dict[str, Any]]:
    out = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def parse_nmap_ports(stdout: str) -> List[str]:
    # simple regex for open ports like "80/tcp open"
    ports = []
    for line in stdout.splitlines():
        m = re.search(r"^(\d+)/(tcp|udp)\s+open", line)
        if m:
            ports.append(f"{m.group(1)}/{m.group(2)}")
    return ports


def extract_assets(output_kind: str, parsed: Any) -> List[str]:
    if output_kind in {"subdomains", "hosts", "urls", "ips", "secrets"}:
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    if output_kind == "ports" and isinstance(parsed, list):
        return [str(x) for x in parsed]
    return []
