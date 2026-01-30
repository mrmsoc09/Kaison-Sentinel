import json
from collections import Counter
from typing import Dict, Any, List

from ..core.config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "deepagents.json"


def _load() -> Dict[str, Any]:
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False}


def deepagents_enabled(kind: str) -> bool:
    cfg = _load()
    return bool(cfg.get("enabled")) and kind in {"osint", "recon"}


def _as_text(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False).lower()
    except Exception:
        return str(value).lower()


def _summarize_artifacts(artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    kind_counts = Counter()
    tool_counts = Counter()
    module_counts = Counter()
    sample_hits: Dict[str, List[str]] = {"endpoints": [], "buckets": [], "auth": [], "config": []}
    for art in artifacts:
        kind = art.get("kind") or art.get("type") or "item"
        kind_counts[kind] += 1
        tool_counts[art.get("tool", "unknown")] += 1
        module_counts[art.get("module", "unknown")] += 1
        text = _as_text(art.get("value", art))
        if "http" in text or "/api" in text:
            if len(sample_hits["endpoints"]) < 10:
                sample_hits["endpoints"].append(text[:200])
        if "s3" in text or "bucket" in text or "storage" in text:
            if len(sample_hits["buckets"]) < 10:
                sample_hits["buckets"].append(text[:200])
        if "login" in text or "auth" in text or "oauth" in text:
            if len(sample_hits["auth"]) < 10:
                sample_hits["auth"].append(text[:200])
        if ".env" in text or "config" in text or "backup" in text:
            if len(sample_hits["config"]) < 10:
                sample_hits["config"].append(text[:200])
    return {
        "kinds": kind_counts.most_common(12),
        "tools": tool_counts.most_common(12),
        "modules": module_counts.most_common(12),
        "samples": sample_hits,
    }


def _derive_hypotheses(artifacts: List[Dict[str, Any]], findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    text_blob = _as_text({"artifacts": artifacts[:50], "findings": findings[:50]})
    hypotheses: List[Dict[str, Any]] = []
    if "subdomain" in text_blob or "dns" in text_blob:
        hypotheses.append({
            "title": "Shadow-IT surface expansion",
            "reason": "Subdomain/DNS artifacts suggest additional assets for ownership and exposure review.",
            "next_step": "Confirm ownership and categorize by business criticality before deeper testing."
        })
    if "s3" in text_blob or "bucket" in text_blob or "storage" in text_blob:
        hypotheses.append({
            "title": "Cloud storage exposure risk",
            "reason": "Storage/bucket indicators present in artifacts.",
            "next_step": "Validate access controls and public access settings with read-only checks."
        })
    if "login" in text_blob or "auth" in text_blob or "oauth" in text_blob:
        hypotheses.append({
            "title": "Authentication surface concentration",
            "reason": "Multiple auth-related endpoints detected.",
            "next_step": "Map auth flows and review for misconfiguration or missing controls."
        })
    if "api" in text_blob or "graphql" in text_blob:
        hypotheses.append({
            "title": "API exposure consolidation",
            "reason": "API endpoints or GraphQL artifacts detected.",
            "next_step": "Inventory endpoints and review access boundaries using safe, read-only probes."
        })
    if any(f.get("severity") in {"high", "critical"} for f in findings):
        hypotheses.append({
            "title": "High-severity validation focus",
            "reason": "High/critical findings present; prioritize evidence collection and validation.",
            "next_step": "Collect non-destructive evidence and prepare HiL validation packets."
        })
    return hypotheses


def _derive_chains(hypotheses: List[Dict[str, Any]], max_branches: int) -> List[Dict[str, Any]]:
    chains: List[Dict[str, Any]] = []
    for idx, h in enumerate(hypotheses[:max_branches]):
        chains.append({
            "id": f"chain-{idx+1}",
            "theme": h.get("title"),
            "steps": [
                "Normalize artifacts into asset inventory.",
                "Triage assets by exposure and business criticality.",
                h.get("next_step"),
                "Queue validation-only checks with HiL gating.",
            ],
        })
    return chains


def run_deepagents(context: Dict[str, Any]) -> Dict[str, Any]:
    cfg = _load()
    artifacts = context.get("artifacts") or []
    findings = context.get("findings") or []
    summary = _summarize_artifacts(artifacts)
    hypotheses = _derive_hypotheses(artifacts, findings)
    chains = _derive_chains(hypotheses, int(cfg.get("max_branches", 5) or 5))

    if not cfg.get("enabled"):
        return {"status": "disabled", "mode": "offline", "summary": summary, "hypotheses": hypotheses, "chains": chains}
    if cfg.get("scope_gated") and not (context.get("scope") or {}).get("allowlist"):
        return {"status": "blocked", "reason": "scope_required", "mode": "offline", "summary": summary, "hypotheses": hypotheses, "chains": chains}
    if cfg.get("hil_required") and not (context.get("scope") or {}).get("validation_confirmed"):
        return {"status": "blocked", "reason": "hil_required", "mode": "offline", "summary": summary, "hypotheses": hypotheses, "chains": chains}

    deepagents_available = True
    try:
        import deepagents  # type: ignore  # optional dependency
        _ = deepagents  # avoid unused
    except Exception:
        deepagents_available = False

    if not context.get("enable_deepagents_run"):
        return {
            "status": "ready",
            "mode": "offline",
            "deepagents_available": deepagents_available,
            "note": "DeepAgents optional; set enable_deepagents_run to execute adapter when configured.",
            "summary": summary,
            "hypotheses": hypotheses,
            "chains": chains,
        }

    return {
        "status": "ok",
        "mode": "offline",
        "deepagents_available": deepagents_available,
        "note": "Offline planning complete. Configure DeepAgents adapter to enable runtime execution.",
        "summary": summary,
        "hypotheses": hypotheses,
        "chains": chains,
    }
