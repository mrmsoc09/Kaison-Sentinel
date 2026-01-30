#!/usr/bin/env python3
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "data" / "vuln_tools.json"
OUT_TOOLS = BASE / "kai11" / "tools"
OUT_JOBS = BASE / "kai11" / "jobs"
OUT_AGENTS = BASE / "kai11" / "agents"
OUT_MODULES = BASE / "kai11" / "modules"
REGISTRY = BASE / "modules" / "registry.json"

for d in [OUT_TOOLS, OUT_JOBS, OUT_AGENTS, OUT_MODULES]:
    d.mkdir(parents=True, exist_ok=True)


def slugify(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", s).lower()


def to_class_name(s: str) -> str:
    parts = re.split(r"[^a-zA-Z0-9]+", s)
    return "".join(p.capitalize() for p in parts if p)


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content)


def tool_template(tool_id: str) -> str:
    cls = to_class_name(tool_id)
    return f"""from typing import Dict, Any\nfrom ..core.tool_exec import run_tool\n\n\nclass {cls}:\n    id = \"{tool_id}\"\n\n    def run(self, target: str) -> Dict[str, Any]:\n        return run_tool(self.id, target)\n"""


def job_template(job_id: str, tool_mod: str, tool_cls: str) -> str:
    return f"""from typing import Dict, Any, List\nfrom ..tools.{tool_mod} import {tool_cls}\n\n\nclass {to_class_name(job_id)}:\n    id = \"{job_id}\"\n\n    def __init__(self):\n        self.tool = {tool_cls}()\n\n    def run(self, targets: List[str]) -> Dict[str, Any]:\n        results = []\n        for t in targets:\n            results.append(self.tool.run(t))\n        return {{\"results\": results}}\n"""


def agent_template(agent_id: str, job_mod: str, job_cls: str) -> str:
    return f"""from typing import Dict, Any, List\nfrom ..jobs.{job_mod} import {job_cls}\nfrom ..core.audit import append_audit\n\n\nclass {to_class_name(agent_id)}:\n    id = \"{agent_id}\"\n\n    def __init__(self):\n        self.job = {job_cls}()\n\n    def run(self, targets: List[str], circle: Dict[str, Any]) -> Dict[str, Any]:\n        append_audit({{\"event\": \"agent_start\", \"agent\": self.id, \"circle\": circle}})\n        result = self.job.run(targets)\n        append_audit({{\"event\": \"agent_done\", \"agent\": self.id}})\n        return result\n"""


def module_template(module_id: str, agent_mod: str, agent_cls: str) -> str:
    return f"""import os\nfrom typing import Dict, Any\nfrom .base import ModuleBase\nfrom ..agents.{agent_mod} import {agent_cls}\nfrom ..orchestrator.circle import select_circle, lang_studio_enabled\n\n\n\ndef _allow_network() -> bool:\n    return os.getenv(\"KAI_ALLOW_NETWORK\") == \"1\"\n\n\nclass {to_class_name(module_id)}(ModuleBase):\n    id = \"{module_id}\"\n    kind = \"vuln\"\n    risk = \"medium\"\n\n    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:\n        return {{\n            \"module\": self.id,\n            \"mode\": \"plan\",\n            \"actions\": [self.id],\n            \"safe_mode\": True,\n            \"circle\": \"vuln\",\n            \"lang_studio\": lang_studio_enabled(\"vuln\"),\n        }}\n\n    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:\n        if not _allow_network():\n            return {{\"module\": self.id, \"mode\": \"execute\", \"results\": [], \"findings\": [], \"note\": \"network_disabled_set_KAI_ALLOW_NETWORK=1\"}}\n        scope = context.get(\"scope\", {{}})\n        targets = scope.get(\"allowlist\") or []\n        circle = select_circle(\"vuln\")\n        agent = {agent_cls}()\n        res = agent.run(targets, circle)\n        return {{\"module\": self.id, \"mode\": \"execute\", \"results\": res.get(\"results\", []), \"findings\": [], \"circle\": circle}}\n"""


obj = json.loads(INPUT.read_text())
items = obj.get("items", [])

registry = {"version": 1, "modules": []}
if REGISTRY.exists():
    registry = json.loads(REGISTRY.read_text())

existing_ids = {m.get("id") for m in registry.get("modules", [])}

for it in items:
    module_id = it["module"]
    agent_id = it["agent"]
    tool_id = it["tool"]
    job_id = it["job"]

    tool_slug = slugify(tool_id)
    job_slug = slugify(job_id)
    agent_slug = slugify(agent_id)
    module_slug = slugify(module_id)

    tool_cls = to_class_name(tool_id)
    job_cls = to_class_name(job_id)
    agent_cls = to_class_name(agent_id)

    write_if_missing(OUT_TOOLS / f"{tool_slug}.py", tool_template(tool_id))
    write_if_missing(OUT_JOBS / f"{job_slug}.py", job_template(job_id, tool_slug, tool_cls))
    write_if_missing(OUT_AGENTS / f"{agent_slug}.py", agent_template(agent_id, job_slug, job_cls))
    write_if_missing(OUT_MODULES / f"{module_slug}.py", module_template(module_id, agent_slug, agent_cls))

    if module_id not in existing_ids:
        registry.setdefault("modules", []).append({
            "id": module_id,
            "kind": "vuln",
            "risk": "medium",
            "supports": ["plan", "execute"],
            "entry": f"kai11.modules.{module_slug}:{to_class_name(module_id)}",
        })

REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2))
print(f"Generated {len(items)} vuln module wrappers")
