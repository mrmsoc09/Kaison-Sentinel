# Guardrails (RBAC + Policy-as-Code)

This build enforces plan-first execution with explicit approval gates, role-based permissions, and policy rules defined in JSON.

## Key files
- `config/policy.json` (roles + defaults)
- `config/policy_rules.json` (deny rules + HiL requirements)
- `config/governance.json` (redaction + evidence immutability)

## Behavior
- Plan mode requires role in {analyst, operator, admin}
- Execute mode requires role in {operator, admin}
- Vuln execute requires admin (policy rule)
- High-risk execute requires admin (policy rule)
- HiL approval required for medium/high/critical

## Usage
- Set role in scope: `{ "allowlist": ["example.com"], "role": "operator", "module_kind": "osint" }`
- Use `--approve` for execute when HiL is required.

Policy rules are evaluated in `kai11/core/policy_engine.py`.
