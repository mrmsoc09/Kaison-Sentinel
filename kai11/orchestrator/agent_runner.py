import json
from typing import Dict, Any, List

from ..agents.core import (
    OrchestratorAgent,
    ReconAgent,
    VulnAgent,
    CorrelationAgent,
    EvidenceAgent,
    MitigationAgent,
    ReportingAgent,
    TrainingAgent,
    GraphAgent,
    PolicyAgent,
    ToolHealthAgent,
    PersonaAgent,
)
from .circle import select_circle
from .deepagents import deepagents_enabled, run_deepagents


AGENT_MAP = {
    "agent.orchestrator": OrchestratorAgent,
    "agent.recon": ReconAgent,
    "agent.vuln": VulnAgent,
    "agent.correlation": CorrelationAgent,
    "agent.evidence": EvidenceAgent,
    "agent.mitigation": MitigationAgent,
    "agent.reporting": ReportingAgent,
    "agent.training": TrainingAgent,
    "agent.graph": GraphAgent,
    "agent.policy": PolicyAgent,
    "agent.toolhealth": ToolHealthAgent,
    "agent.persona": PersonaAgent,
}


def _agent_list_for_kind(kind: str) -> List[str]:
    base = [
        "agent.orchestrator",
        "agent.policy",
        "agent.toolhealth",
        "agent.persona",
        "agent.correlation",
        "agent.evidence",
        "agent.reporting",
        "agent.mitigation",
        "agent.graph",
        "agent.training",
    ]
    if kind in {"osint", "recon"}:
        return ["agent.recon"] + base
    if kind == "vuln":
        return ["agent.vuln"] + base
    return ["agent.recon", "agent.vuln"] + base


def run_orchestration(context: Dict[str, Any]) -> Dict[str, Any]:
    kind = context.get("module_kind", "all")
    domain = "osint" if kind in {"osint", "recon"} else ("vuln" if kind == "vuln" else "osint")
    circle = select_circle(domain)
    ctx = dict(context)
    ctx["circle"] = circle

    results = []
    deepagents_result = None
    if deepagents_enabled(domain):
        deepagents_result = run_deepagents(ctx)
    for agent_id in _agent_list_for_kind(kind):
        cls = AGENT_MAP.get(agent_id)
        if not cls:
            continue
        agent = cls()
        res = agent.run(ctx)
        results.append(res)

    return {"circle": circle, "agents": results, "deepagents": deepagents_result}
