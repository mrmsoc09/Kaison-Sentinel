import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kai11.core.scan_engine import run_plan, run_execute


def main():
    scope = {
        "allowlist": ["example.com"],
        "goal": "Vulnerability smoke test",
        "constraints": "plan-first",
        "module_kind": "vuln",
        "role": "admin",
        "validation_confirmed": False,
    }
    os.environ.setdefault("KAI_ALLOW_PLAINTEXT", "1")
    print("Planning vuln...")
    plan = run_plan(scope)
    print("Plan ok:", plan.get("run_id"))

    os.environ.setdefault("KAI_ALLOW_NETWORK", "0")
    os.environ.setdefault("KAI_ALLOW_ACTIVE", "0")
    print("Executing (network gated)...")
    exec_out = run_execute(scope, approved=True, mitigation_tier="minimal")
    print("Execute status:", exec_out.get("status"))
    print("Run id:", exec_out.get("run_id"))
    print("Report:", exec_out.get("report"))
    print("Report blocked reason:", exec_out.get("run_record"))


if __name__ == "__main__":
    main()
