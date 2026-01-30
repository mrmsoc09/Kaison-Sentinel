import os
import platform
from typing import Dict


def _read_meminfo() -> Dict[str, int]:
    info: Dict[str, int] = {}
    path = "/proc/meminfo"
    if not os.path.exists(path):
        return info
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                parts = line.split(":")
                if len(parts) != 2:
                    continue
                key = parts[0].strip()
                value = parts[1].strip().split()[0]
                if value.isdigit():
                    info[key] = int(value)
    except Exception:
        return info
    return info


def hardware_profile() -> Dict[str, str | int | float]:
    mem = _read_meminfo()
    mem_total_kb = mem.get("MemTotal", 0)
    mem_avail_kb = mem.get("MemAvailable", 0)
    cpu = os.cpu_count() or 2
    return {
        "platform": platform.system().lower(),
        "platform_release": platform.release(),
        "cpu_count": cpu,
        "mem_total_gb": round(mem_total_kb / 1024 / 1024, 2) if mem_total_kb else 0,
        "mem_available_gb": round(mem_avail_kb / 1024 / 1024, 2) if mem_avail_kb else 0,
    }
