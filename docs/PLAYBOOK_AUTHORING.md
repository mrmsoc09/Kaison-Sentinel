# Playbook Authoring Guide

A playbook is a JSON file that lists modules to run in order.

## Example
```
{
  "id": "playbook.osint.basic",
  "name": "OSINT Basic",
  "version": "1.0",
  "modules": [
    "osint.subdomain.amass",
    "osint.web.httpx",
    "osint.web.waybackurls"
  ],
  "tags": ["osint", "basic"]
}
```

## Validation
```
python3 -m kai11.assets_cli --validate playbooks --path config/playbooks/osint.basic.json
```

## Conventions
- Use stable module IDs from `modules/registry.json`
- Keep playbooks small and composable
- Prefer safe-mode tools in default playbooks
