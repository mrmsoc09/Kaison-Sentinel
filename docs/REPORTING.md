# Reporting Module

Reports can be generated in Markdown/JSON/SARIF using templates under `config/report_formats/`.

## Selection
Use `report_format_id` in scope or choose in UI.

## Validation
For vuln runs, reports are blocked until `validation_confirmed: true`.
