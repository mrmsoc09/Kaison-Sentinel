import hashlib
from typing import List, Dict, Any

from .contracts import Finding, EvidenceRef

SEVERITY_ORDER = ["info", "low", "medium", "high", "critical"]


def _hash_finding(title: str, target: str) -> str:
    raw = f"{title}|{target}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def normalize_findings(raw: List[Dict[str, Any]], target: str) -> List[Finding]:
    out: List[Finding] = []
    for r in raw:
        title = r.get("title") or "Unspecified Finding"
        sev = (r.get("severity") or "info").lower()
        if sev not in SEVERITY_ORDER:
            sev = "info"
        confidence = float(r.get("confidence") or 0.5)
        signals = int(r.get("signals") or 1)
        ev = r.get("evidence") or []
        evid = [EvidenceRef(kind=e.get("kind", "raw"), path=e.get("path", "")) for e in ev]
        fid = r.get("id") or _hash_finding(title, target)
        out.append(Finding(
            id=fid,
            title=title,
            severity=sev,
            confidence=confidence,
            target=target,
            evidence=evid,
            status=r.get("status", "signal"),
            signals=signals,
            intel_state=r.get("intel_state", "raw"),
            labels=r.get("labels", []),
            repro_steps=r.get("repro_steps", []),
            duplicate_risk=r.get("duplicate_risk", "low"),
            duplicate_matches=int(r.get("duplicate_matches") or 0),
            duplicate_validated=int(r.get("duplicate_validated") or 0),
        ))
    return out


def dedupe_findings(findings: List[Finding]) -> List[Finding]:
    precedence = ["invalid", "hypothesis", "signal", "likely", "validated"]
    by_key: Dict[tuple, Finding] = {}
    out: List[Finding] = []
    for f in findings:
        key = (f.title, f.target, f.severity)
        if key not in by_key:
            by_key[key] = f
            out.append(f)
            continue
        existing = by_key[key]
        existing.signals += f.signals
        existing.confidence = max(existing.confidence, f.confidence)
        # Merge evidence (dedupe by kind+path)
        ev_seen = {(e.kind, e.path) for e in existing.evidence}
        for e in f.evidence:
            if (e.kind, e.path) not in ev_seen:
                existing.evidence.append(e)
                ev_seen.add((e.kind, e.path))
        # Merge labels
        for label in f.labels:
            if label not in existing.labels:
                existing.labels.append(label)
        # Merge status by precedence
        if precedence.index(f.status) > precedence.index(existing.status):
            existing.status = f.status
    return out


def score_confidence(findings: List[Finding]) -> List[Finding]:
    for f in findings:
        if f.severity in {"high", "critical"}:
            f.confidence = min(1.0, f.confidence + 0.1)
        if f.signals >= 2:
            f.confidence = min(1.0, f.confidence + 0.1)
    return findings


def apply_signal_threshold(findings: List[Finding]) -> List[Finding]:
    # Require at least 2 signals for high/critical confidence
    for f in findings:
        if f.severity in {"high", "critical"} and f.signals < 2:
            f.severity = "medium"
            f.status = "signal"
            f.confidence = min(f.confidence, 0.6)
    return findings
