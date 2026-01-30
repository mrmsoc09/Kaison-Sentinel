# Webhooks

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

Webhooks are disabled by default. When enabled, events are POSTed as JSON to configured endpoints.

Config: `config/webhooks.json`

Events:
- `run.completed`
- `alert.raised`
- `hil.overdue`

Payload:
```
{
  "event": "run.completed",
  "payload": { ... }
}
```
