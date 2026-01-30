# Data Retention

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

Retention is disabled by default. When enabled, files are **archived** (not deleted) unless explicitly configured.

Config: `config/retention.json`

```
{
  "enabled": true,
  "action": "archive",
  "days": {
    "runs": 30,
    "reports": 60,
    "evidence": 60
  }
}
```

Actions:
- `archive`: move files to `outputs/archive/`
- `delete`: permanently remove files (use with caution)
