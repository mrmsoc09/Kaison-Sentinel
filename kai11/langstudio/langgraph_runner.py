import json
from typing import Dict, Any, List, TypedDict

from ..core.config import LANGSTUDIO_DIR

LANGSTUDIO_DIR.mkdir(parents=True, exist_ok=True)


class GraphState(TypedDict):
    artifacts: List[dict]
    summary: str
    triage: List[dict]
    ranked: List[dict]


def _summarize(artifacts: List[dict]) -> str:
    counts: Dict[str, int] = {}
    for a in artifacts:
        kind = a.get("kind") or a.get("type") or "item"
        counts[kind] = counts.get(kind, 0) + 1
    parts = [f"{k}:{v}" for k, v in sorted(counts.items())]
    return "artifact_counts=" + ",".join(parts) if parts else "no_artifacts"


def _triage(artifacts: List[dict]) -> List[dict]:
    triaged = []
    for a in artifacts:
        score = 0
        txt = json.dumps(a, ensure_ascii=False).lower()
        if "password" in txt or "token" in txt:
            score += 2
        if a.get("kind") in {"endpoint", "port", "subdomain"} or a.get("type") in {"endpoint", "port", "subdomain"}:
            score += 1
        triaged.append({"artifact": a, "score": score})
    triaged.sort(key=lambda x: x["score"], reverse=True)
    return triaged[:25]


def _rank(triage: List[dict]) -> List[dict]:
    return triage


def run_langgraph(domain: str, module_id: str, artifacts: List[dict]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "domain": domain,
        "module": module_id,
        "artifacts": len(artifacts),
        "status": "planned",
    }
    try:
        from langgraph.graph import StateGraph  # type: ignore

        graph = StateGraph(GraphState)

        def step_summarize(state: GraphState) -> GraphState:
            return {**state, "summary": _summarize(state["artifacts"])}

        def step_triage(state: GraphState) -> GraphState:
            return {**state, "triage": _triage(state["artifacts"])}

        def step_rank(state: GraphState) -> GraphState:
            return {**state, "ranked": _rank(state["triage"])}

        graph.add_node("summarize", step_summarize)
        graph.add_node("triage", step_triage)
        graph.add_node("rank", step_rank)
        graph.add_edge("summarize", "triage")
        graph.add_edge("triage", "rank")
        graph.set_entry_point("summarize")

        runner = graph.compile()
        state: GraphState = {"artifacts": artifacts, "summary": "", "triage": [], "ranked": []}
        out = runner.invoke(state)
        payload = {
            "domain": domain,
            "module": module_id,
            "status": "ok",
            "summary": out.get("summary"),
            "triage": out.get("triage"),
            "ranked": out.get("ranked"),
        }
    except Exception as e:
        payload["status"] = "fallback"
        payload["error"] = str(e)

    path = LANGSTUDIO_DIR / f"langgraph_{domain}_{module_id}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload
