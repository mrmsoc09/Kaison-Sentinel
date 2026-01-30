# Technical Requirements

1) All prompts, personas, playbooks, and report formats must be JSON-defined and validated.
2) All prompts must support placeholder substitution with validation for missing variables.
3) Prompt, persona, playbook, and report format registries must be listable and previewable via CLI.
4) Routing must select defaults by module kind and vertical, with overrides by id.
5) Report templates must support Markdown/JSON/SARIF rendering.
6) Adapter classes must include Strategic Intent docstrings:
   - GoogleSCCAdapter: "Purpose: Provide visibility to Cloud Governance teams."
   - AWSSecurityHubAdapter: "Purpose: Enable automated Lambda-based remediation."
   - SarifAdapter: "Purpose: Provide line-of-code feedback to developers in PRs."
7) Optional pgvector backend for enterprise scalability with file-store fallback.
