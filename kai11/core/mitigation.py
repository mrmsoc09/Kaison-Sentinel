from typing import List, Dict
import json
from pathlib import Path

from .contracts import MitigationBlock
from .config import BUILD_ROOT

TEMPLATES = BUILD_ROOT / "config" / "mitigation_templates.json"


def _load_templates() -> List[Dict]:
    if not TEMPLATES.exists():
        return []
    try:
        return json.loads(TEMPLATES.read_text()).get("rules", [])
    except Exception:
        return []


def _apply_templates(title: str, block: MitigationBlock) -> None:
    t = title.lower()
    for rule in _load_templates():
        if any(k in t for k in rule.get("match", [])):
            block.dry_run_cmds.extend(rule.get("dry_run", []))
            block.apply_cmds.extend(rule.get("apply", []))
            block.verify_steps.extend(rule.get("verify", []))
            block.rollback_steps.extend(rule.get("rollback", []))
            if rule.get("code_fix"):
                block.code_fix = rule.get("code_fix")


def _ubuntu_dry_run() -> List[str]:
    return [
        "uname -a",
        "lsb_release -a",
        "systemctl status <service>",
        "dpkg -l | grep <package>",
    ]


def _ubuntu_apply() -> List[str]:
    return [
        "sudo apt-get update",
        "sudo apt-get install --only-upgrade <package>",
        "sudo systemctl restart <service>",
    ]


def _cloud_dry_run() -> Dict[str, List[str]]:
    return {
        "gcp": ["gcloud asset search-all-resources --scope=projects/<project-id> --query=<query>"],
        "aws": ["aws resourcegroupstaggingapi get-resources --tag-filters Key=<key>,Values=<value>"],
        "azure": ["az resource list --query <query>"],
        "cloudflare": ["cf zones list"],
    }


def _cloud_apply() -> Dict[str, List[str]]:
    return {
        "gcp": ["gcloud <service> <resource> update <flags>"],
        "aws": ["aws <service> update-<resource> --<flags>"],
        "azure": ["az <service> update --<flags>"],
        "cloudflare": ["cf <resource> update <id> --<flags>"],
    }


def generate_mitigation(tier: str = "standard", title: str | None = None) -> MitigationBlock:
    tier = tier.lower()
    dry = _ubuntu_dry_run()
    apply_cmds = _ubuntu_apply()

    verify = [
        "cat /var/log/syslog | tail -n 200",
        "systemctl status <service>",
        "curl -I <endpoint>",
    ]
    rollback = [
        "sudo apt-get install <package>=<previous-version>",
        "sudo systemctl restart <service>",
    ]
    rotation = [
        "rotate credentials via your secrets manager",
        "revoke old tokens and re-issue",
    ]

    cloud_dry = _cloud_dry_run()
    cloud_apply = _cloud_apply()

    block = MitigationBlock(
        tier=tier if tier in {"standard", "deep", "minimal"} else "standard",
        dry_run_cmds=dry,
        apply_cmds=apply_cmds,
        verify_steps=verify,
        rollback_steps=rollback,
        rotation_steps=rotation,
        cloud_cmds={"dry_run": cloud_dry, "apply": cloud_apply},
    )

    if tier == "deep":
        block.verify_steps.append("run unit/integration tests for affected services")
        block.rollback_steps.append("restore config from backup and re-run verification")

    if title:
        _apply_templates(title, block)

    return block
