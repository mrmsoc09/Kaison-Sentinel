import json
from typing import Dict, Any, List

from ..core.audit import append_audit
from ..core.redact import redact_text
from ..core.config import BUILD_ROOT
from .tracing import record_trace
from .langgraph_runner import run_langgraph

CONF = BUILD_ROOT / "config" / "langstudio.json"


def _load_flows() -> Dict[str, List[str]]:
    try:
        data = json.loads(CONF.read_text())
        return data.get("flows", {})
    except Exception:
        return {}


def _summarize(artifacts: List[Dict[str, Any]]) -> str:
    counts: Dict[str, int] = {}
    for a in artifacts:
        kind = a.get("kind", "item")
        counts[kind] = counts.get(kind, 0) + 1
    parts = [f"{k}:{v}" for k, v in sorted(counts.items())]
    return "artifact_counts=" + ",".join(parts) if parts else "no_artifacts"


def _triage(artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    triaged = []
    for a in artifacts:
        score = 0
        text = json.dumps(a, ensure_ascii=False)
        if "password" in text.lower() or "token" in text.lower():
            score += 2
        if a.get("kind") in {"endpoint", "port", "subdomain"}:
            score += 1
        triaged.append({"artifact": a, "score": score})
    triaged.sort(key=lambda x: x["score"], reverse=True)
    return triaged[:25]


def run_flow(domain: str, module_id: str, artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    flows = _load_flows()
    steps = flows.get(domain, ["summarize", "triage", "rank", "mitigate"])
    summary = _summarize(artifacts)
    triaged = _triage(artifacts)
    notes = redact_text(summary)
    append_audit({"event": "langstudio_flow", "domain": domain, "module": module_id, "summary": notes})
    trace_path = record_trace({"domain": domain, "module": module_id, "steps": steps, "summary": notes})
    langgraph = run_langgraph(domain, module_id, artifacts)
    return {
        "domain": domain,
        "module": module_id,
        "steps": steps,
        "summary": notes,
        "triage": triaged,
        "trace": trace_path,
        "langgraph": langgraph,
    }
