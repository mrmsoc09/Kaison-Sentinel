# Customization Guide (Playbooks, Personas, Prompts)

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Directories
- `config/playbooks/` — playbook JSON
- `config/personas/` — persona JSON
- `config/prompts/` — system/scan/report prompts
- `config/report_formats/` — report templates
- `config/schemas/` — JSON schemas

## CLI
List assets:
```
python3 -m kai11.assets_cli --list prompts
python3 -m kai11.assets_cli --list personas
python3 -m kai11.assets_cli --list playbooks
python3 -m kai11.assets_cli --list report_formats
```

Validate an asset:
```
python3 -m kai11.assets_cli --validate prompts --path config/prompts/scan.default.json
```

## Prompt placeholders
Common placeholders:
- `{goal}`
- `{scope}`
- `{mode}`
- `{modules}`
- `{constraints}`

## Routing
- `core/routing.py` chooses default persona and prompts per context
- Provide `persona_id`, `module_kind`, `vertical` in scope for custom routing

## Reporting
- Use `report_format_id` in scope to select `config/report_formats/*.json`
