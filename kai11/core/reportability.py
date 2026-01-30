from typing import List
from .contracts import Finding


def score_reportability(findings: List[Finding], module_kind: str) -> List[Finding]:
    for f in findings:
        base = f.confidence * 100
        if module_kind in {"osint", "recon"}:
            if f.signals >= 2:
                base += 10
            if f.severity in {"high", "critical"}:
                base += 15
        f.reportability = max(0.0, min(100.0, base))
    return findings
