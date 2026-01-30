# Webhooks

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
