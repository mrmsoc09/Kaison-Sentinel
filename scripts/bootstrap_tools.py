#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kai11.core.tool_health import write_health_report

if __name__ == "__main__":
    path = write_health_report(check_version=False)
    print(f"tool health report written to {path}")
