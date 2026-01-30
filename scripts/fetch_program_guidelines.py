#!/usr/bin/env python3
"""
Fetch scope and policy pages for public bug bounty programs.

Outputs per-program folders with scope/policy HTML and text, plus meta.json.
This script is intended to be run by the operator with network access.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kai11.core.program_sync import sync_program_scopes  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sleep", type=float, default=1.5, help="Delay between requests (seconds)")
    ap.add_argument("--respect-config", action="store_true", help="Respect program_sync.enabled")
    ap.add_argument("--allow-network", action="store_true", help="Allow network access for sync")
    args = ap.parse_args()

    res = sync_program_scopes(
        allow_network=args.allow_network or None,
        sleep_seconds=args.sleep,
        force=not args.respect_config,
    )
    print(res)
    return 0 if res.get("status") in {"ok", "disabled"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
