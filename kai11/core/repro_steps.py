from typing import List, Dict, Any

from .contracts import Finding


def _target(scope: Dict[str, Any], finding: Finding) -> str:
    return finding.target or (scope.get("allowlist") or [""])[0]


def build_repro_steps(finding: Finding, scope: Dict[str, Any]) -> List[str]:
    target = _target(scope, finding)
    labels = set(finding.labels or [])
    steps: List[str] = []

    # Generic safe reproduction skeleton
    steps.append("Preconditions: Confirm target is in scope and safe-mode rules apply.")
    steps.append(f"Target: {target}")

    if any(l.startswith("tool:tool.nuclei") for l in labels):
        steps.append(f"CLI: nuclei -u {target} -jsonl -severity medium,high,critical")
        steps.append("Expected: JSONL output contains the matched template and target URL.")
    elif any(l.startswith("tool:tool.nikto") for l in labels):
        steps.append(f"CLI: nikto -host {target}")
        steps.append("Expected: Nikto output flags the vulnerability with evidence lines.")
    elif any(l.startswith("tool:tool.sqlmap") for l in labels):
        steps.append(f"CLI: sqlmap -u {target} --batch --crawl=1 --risk=1 --level=1")
        steps.append("Expected: sqlmap reports injection points without destructive actions.")
    elif "xss" in finding.title.lower() or "xss" in " ".join(labels):
        steps.append(f"CLI: curl -s '{target}?q=%3Cscript%3Ealert(1)%3C/script%3E'")
        steps.append("Expected: response reflects payload (sanitize verification).")
    elif "sql" in finding.title.lower() or "sqli" in " ".join(labels):
        steps.append(f"CLI: curl -s '{target}?id=1%27%20OR%201=1--' | head -n 5")
        steps.append("Expected: response differs from baseline (read-only check).")
    elif "header" in finding.title.lower():
        steps.append(f"CLI: curl -I {target}")
        steps.append("Expected: missing security headers are confirmed.")
    else:
        steps.append(f"CLI: curl -I {target}")
        steps.append("Expected: evidence in headers/body aligns with finding.")

    steps.append("Capture screen recording of the reproduction steps and attach it before submission.")
    return steps
