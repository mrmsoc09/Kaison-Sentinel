import json
import os
import shutil
import subprocess
from typing import Dict, Any

from .config import BUILD_ROOT
from .audit import append_audit
from .parsers import parse_lines, parse_json, parse_jsonl, parse_nmap_ports, extract_assets
from .limits import rate_limit
from .tool_policy import tool_allowed
from .hooks import before_tool, after_tool
from .tool_registry import category_meta

CONF_OSINT = BUILD_ROOT / "config" / "tools_osint.json"
CONF_VULN = BUILD_ROOT / "config" / "tools_vuln.json"


def _load_conf() -> Dict[str, Any]:
    tools = []
    for conf in [CONF_OSINT, CONF_VULN]:
        try:
            data = json.loads(conf.read_text())
            tools.extend(data.get("tools", []))
        except Exception:
            continue
    return {"version": 1, "tools": tools}


def _find_tool(tool_id: str) -> Dict[str, Any] | None:
    conf = _load_conf()
    for t in conf.get("tools", []):
        if t.get("tool_id") == tool_id:
            return t
    return None


def _format_args(t: Dict[str, Any], target: str) -> list[str]:
    binary = t.get("binary")
    args = t.get("args_template", [])
    # parameter defaults
    env = {
        "binary": binary,
        "target": target,
        "wordlist": os.getenv("KAI_WORDLIST", "/usr/share/wordlists/dirb/common.txt"),
        "threads": os.getenv("KAI_THREADS", "25"),
        "rate": os.getenv("KAI_RATE", "10"),
    }
    out = []
    for a in args:
        out.append(a.format(**env))
    return out


def _parse_output(parser: str, stdout: str):
    if parser == "jsonl":
        return parse_jsonl(stdout)
    if parser == "json":
        return parse_json(stdout)
    if parser == "nmap":
        return parse_nmap_ports(stdout)
    return parse_lines(stdout)


def run_tool(tool_id: str, target: str, options: Dict[str, Any] | None = None) -> Dict[str, Any]:
    t = _find_tool(tool_id)
    if not t:
        return {"tool": tool_id, "status": "missing_config"}

    binary = t.get("binary")
    if not binary:
        return {"tool": tool_id, "status": "missing_binary"}

    if not os.getenv("KAI_ALLOW_NETWORK") == "1":
        return {"tool": tool_id, "status": "blocked", "reason": "network_disabled"}

    if t.get("active") and not os.getenv("KAI_ALLOW_ACTIVE") == "1":
        return {"tool": tool_id, "status": "blocked", "reason": "active_requires_KAI_ALLOW_ACTIVE"}

    category = t.get("category", "")
    if options:
        if not tool_allowed(category, options):
            return {"tool": tool_id, "status": "blocked", "reason": "category_not_allowed", "category": category}

    if not shutil.which(binary):
        return {"tool": tool_id, "status": "missing_binary", "binary": binary}

    meta = category_meta(category)
    pre = before_tool(tool_id, target, meta)
    if not pre.get("allowed", True):
        return {"tool": tool_id, "status": "blocked", "reason": pre.get("reason", "blocked_by_hook")}

    cmd = _format_args(t, target)
    timeout = int(t.get("timeout") or 120)
    parser = t.get("parser") or "lines"
    output_kind = t.get("output_kind") or "items"

    append_audit({"event": "tool_run", "tool": tool_id, "cmd": cmd})
    try:
        rate_limit(options=options, tool_id=tool_id)
        env = os.environ.copy()
        extra_bin = str(BUILD_ROOT / "tools" / "bin")
        env["PATH"] = f"{extra_bin}:{env.get('PATH', '')}"
        if options:
            proxy = options.get("proxy") or {}
            if proxy.get("http"):
                env["HTTP_PROXY"] = proxy.get("http")
            if proxy.get("https"):
                env["HTTPS_PROXY"] = proxy.get("https")
            if proxy.get("no_proxy"):
                env["NO_PROXY"] = proxy.get("no_proxy")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
        stdout = result.stdout[-20000:]
        stderr = result.stderr[-20000:]
        parsed = _parse_output(parser, stdout)
        assets = extract_assets(output_kind, parsed)
        result_out = {
            "tool": tool_id,
            "target": target,
            "status": "ok" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "parser": parser,
            "output_kind": output_kind,
            "parsed": parsed,
            "assets": assets,
            "category": category,
            "risk": meta.get("risk", "low"),
            "evidence_kind": meta.get("evidence_kind", "raw"),
        }
        if options and options.get("langstudio", {}).get("wrap_tools"):
            result_out.setdefault("langstudio", {})
            result_out["langstudio"].update({"wrapped": True, "module": t.get("module_id")})
        return after_tool(tool_id, target, result_out)
    except subprocess.TimeoutExpired:
        return {"tool": tool_id, "status": "timeout"}
    except Exception as e:
        return {"tool": tool_id, "status": "error", "error": str(e)}
