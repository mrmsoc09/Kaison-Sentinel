import json
from pathlib import Path
from typing import Dict, Any, List

from .config import OUTPUT_DIR


def build_graph(artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    nodes = []
    edges = []
    seen_nodes = set()

    def add_node(node_id: str, ntype: str, value: str):
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        nodes.append({"id": node_id, "type": ntype, "value": value})

    for a in artifacts:
        t = a.get("type")
        v = str(a.get("value"))
        tgt = a.get("target")
        node_id = f"{t}:{v}"
        add_node(node_id, t, v)
        if tgt:
            tnode = f"target:{tgt}"
            add_node(tnode, "target", tgt)
            edges.append({"src": tnode, "dst": node_id, "type": "observed"})

    return {"nodes": nodes, "edges": edges}


def write_graph(run_id: str, artifacts: List[Dict[str, Any]]) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graph = build_graph(artifacts)
    path = OUTPUT_DIR / f"{run_id}_graph.json"
    path.write_text(json.dumps(graph, ensure_ascii=False, indent=2))
    return str(path)
