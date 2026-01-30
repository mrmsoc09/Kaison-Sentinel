# Vulnerability Core Install (Local)

- Script: `scripts/install_vuln_core.sh`
- Notes:
  - Installs baseline tools: nmap, nikto, sqlmap, masscan, nuclei, semgrep, bandit, pip-audit, zap-cli.
  - Some tools (e.g., OpenVAS/GVM, Arachni, WPSCAN, MobSF) require heavier setup and are intentionally left as manual/optional steps.
  - Run with sudo, or adjust for your environment.

Recommended:
- Run OSINT core install first if you want shared tooling.
- Verify tool health via `/api/tools/health` or UI “Tool Health” panel.
