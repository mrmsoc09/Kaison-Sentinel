#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "data" / "vuln_tools.json"
OUT = BASE / "config" / "tools_vuln.json"

TOOL_META = {
    "tool.nikto": {
        "binary": "nikto",
        "args_template": ["{binary}", "-host", "{target}"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.nuclei": {
        "binary": "nuclei",
        "args_template": ["{binary}", "-u", "{target}", "-jsonl"],
        "parser": "jsonl",
        "output_kind": "findings",
        "active": True,
    },
    "tool.zap_cli": {
        "binary": "zap-cli",
        "args_template": ["{binary}", "quick-scan", "--self-contained", "--spider", "-l", "medium", "{target}"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.arachni": {
        "binary": "arachni",
        "args_template": ["{binary}", "{target}"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.sqlmap": {
        "binary": "sqlmap",
        "args_template": ["{binary}", "-u", "{target}", "--batch", "--crawl=1"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.wpscan": {
        "binary": "wpscan",
        "args_template": ["{binary}", "--url", "{target}", "--enumerate", "vp,vt,cb,dbe"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.dirsearch": {
        "binary": "dirsearch",
        "args_template": ["{binary}", "-u", "{target}", "-e", "*"],
        "parser": "lines",
        "output_kind": "endpoints",
        "active": True,
    },
    "tool.gobuster": {
        "binary": "gobuster",
        "args_template": ["{binary}", "dir", "-u", "{target}", "-w", "{wordlist}"],
        "parser": "lines",
        "output_kind": "endpoints",
        "active": True,
    },
    "tool.ffuf": {
        "binary": "ffuf",
        "args_template": ["{binary}", "-u", "{target}/FUZZ", "-w", "{wordlist}"],
        "parser": "lines",
        "output_kind": "endpoints",
        "active": True,
    },
    "tool.xsstrike": {
        "binary": "xsstrike",
        "args_template": ["{binary}", "-u", "{target}", "--crawl"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.nmap_vuln": {
        "binary": "nmap",
        "args_template": ["{binary}", "-sV", "--script", "vuln", "{target}"],
        "parser": "nmap",
        "output_kind": "ports",
        "active": True,
    },
    "tool.rustscan": {
        "binary": "rustscan",
        "args_template": ["{binary}", "-a", "{target}", "--", "-sV"],
        "parser": "lines",
        "output_kind": "ports",
        "active": True,
    },
    "tool.masscan": {
        "binary": "masscan",
        "args_template": ["{binary}", "-p1-1000", "{target}", "--rate", "{rate}"],
        "parser": "lines",
        "output_kind": "ports",
        "active": True,
    },
    "tool.gvm": {
        "binary": "gvm-cli",
        "args_template": ["{binary}", "--gmp-username", "admin", "--gmp-password", "admin", "socket", "--xml", "<get_tasks/>"],
        "parser": "lines",
        "output_kind": "findings",
        "active": True,
    },
    "tool.trivy": {
        "binary": "trivy",
        "args_template": ["{binary}", "image", "{target}", "--quiet", "--format", "json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.grype": {
        "binary": "grype",
        "args_template": ["{binary}", "{target}", "-o", "json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.syft": {
        "binary": "syft",
        "args_template": ["{binary}", "{target}", "-o", "json"],
        "parser": "json",
        "output_kind": "sbom",
        "active": False,
    },
    "tool.osv_scanner": {
        "binary": "osv-scanner",
        "args_template": ["{binary}", "-r", "{target}", "-o", "json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.dependency_check": {
        "binary": "dependency-check",
        "args_template": ["{binary}", "--scan", "{target}", "--format", "JSON"],
        "parser": "lines",
        "output_kind": "findings",
        "active": False,
    },
    "tool.npm_audit": {
        "binary": "npm",
        "args_template": ["{binary}", "audit", "--json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.pip_audit": {
        "binary": "pip-audit",
        "args_template": ["{binary}", "-f", "json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.semgrep": {
        "binary": "semgrep",
        "args_template": ["{binary}", "--config", "auto", "--json", "{target}"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.bandit": {
        "binary": "bandit",
        "args_template": ["{binary}", "-r", "{target}", "-f", "json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.gosec": {
        "binary": "gosec",
        "args_template": ["{binary}", "-fmt", "json", "{target}"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.brakeman": {
        "binary": "brakeman",
        "args_template": ["{binary}", "-f", "json", "{target}"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.tfsec": {
        "binary": "tfsec",
        "args_template": ["{binary}", "--format", "json", "{target}"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.checkov": {
        "binary": "checkov",
        "args_template": ["{binary}", "-d", "{target}", "-o", "json"],
        "parser": "json",
        "output_kind": "findings",
        "active": False,
    },
    "tool.mobfs": {
        "binary": "mobfs",
        "args_template": ["{binary}", "--input", "{target}"],
        "parser": "lines",
        "output_kind": "findings",
        "active": False,
    },
    "tool.binwalk": {
        "binary": "binwalk",
        "args_template": ["{binary}", "{target}"],
        "parser": "lines",
        "output_kind": "artifacts",
        "active": False,
    }
}


def build_tools():
    data = json.loads(INPUT.read_text())
    tools = []
    for item in data.get("items", []):
        tool_id = item["tool"]
        module_id = item["module"]
        meta = TOOL_META.get(tool_id, {})
        tools.append({
            "tool_id": tool_id,
            "module_id": module_id,
            "binary": meta.get("binary", tool_id.replace("tool.", "")),
            "category": module_id.split(".")[1] if "." in module_id else "vuln",
            "active": bool(meta.get("active", False)),
            "args_template": meta.get("args_template", ["{binary}", "{target}"]),
            "timeout": 300 if meta.get("active", False) else 120,
            "parser": meta.get("parser", "lines"),
            "output_kind": meta.get("output_kind", "findings"),
        })
    return {"version": 1, "tools": tools}


if __name__ == "__main__":
    OUT.write_text(json.dumps(build_tools(), ensure_ascii=False, indent=2))
    print(f"wrote {OUT}")
