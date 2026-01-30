# OSINT Tool Readiness Checklist

Use this checklist to verify OSINT tooling before a run.

## Core prerequisites
- `python3` available
- `openssl` available (vault + encryption)

## Common OSINT tools
- Subdomain: amass, subfinder, assetfinder
- HTTP probing: httpx, httprobe
- DNS: dnsx, massdns, puredns
- Screenshots: gowitness, eyewitness, aquatone
- Content discovery: ffuf, gobuster, dirsearch
- OSINT frameworks: spiderfoot, recon-ng

## Install guidance
Install tools via your preferred method (apt, pip, go install). Use substitutes listed in `config/tool_substitutes.json` if a tool is missing.
