import hashlib
from typing import Dict, Any, List


def _key_for_artifact(artifact: Dict[str, Any]) -> str:
    t = artifact.get("type")
    v = artifact.get("value")
    raw = f"{t}|{v}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def correlate_artifacts(artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    buckets: Dict[str, List[Dict[str, Any]]] = {}
    for a in artifacts:
        key = _key_for_artifact(a)
        buckets.setdefault(key, []).append(a)

    signals: List[Dict[str, Any]] = []
    for key, group in buckets.items():
        if len(group) < 2:
            continue
        a0 = group[0]
        signals.append({
            "id": f"signal-{key}",
            "title": f"Correlated artifact ({a0.get('type')})",
            "severity": "info",
            "confidence": min(0.95, 0.5 + 0.1 * len(group)),
            "target": a0.get("target"),
            "status": "signal",
            "evidence": [{"kind": "artifact", "path": a0.get("type", "") }],
            "signals": len(group),
            "artifact_type": a0.get("type"),
        })
    return signals


def chain_signals(artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Simple chaining: subdomain + endpoint on same target
    subs = {a.get("value") for a in artifacts if a.get("type") in {"subdomains", "subdomain"}}
    endpoints = {a.get("value") for a in artifacts if a.get("type") in {"endpoints", "endpoint"}}
    if not subs or not endpoints:
        return []
    return [{
        "id": "chain-subdomain-endpoint",
        "title": "Potential chain: subdomain discovery + endpoint exposure",
        "severity": "low",
        "confidence": 0.6,
        "target": "multiple",
        "status": "signal",
        "evidence": [{"kind": "chain", "path": "subdomain+endpoint"}],
        "signals": min(len(subs), len(endpoints)),
    }]
