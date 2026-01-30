import argparse
import json
from typing import Dict

from .core.scan_engine import run_plan, run_execute


def _parse_scope(arg: str) -> Dict:
    try:
        return json.loads(arg)
    except Exception:
        return {"allowlist": [arg]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["plan", "execute"], default="plan")
    p.add_argument("--scope", required=True, help="JSON scope or single target string")
    p.add_argument("--approve", action="store_true")
    p.add_argument("--tier", default="standard")
    p.add_argument("--kind", choices=["osint", "vuln", "all"], default="all")
    p.add_argument("--role", default="operator")
    args = p.parse_args()

    scope = _parse_scope(args.scope)
    scope["module_kind"] = args.kind
    scope["role"] = args.role
    if args.mode == "plan":
        out = run_plan(scope)
    else:
        out = run_execute(scope, approved=args.approve, mitigation_tier=args.tier)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
