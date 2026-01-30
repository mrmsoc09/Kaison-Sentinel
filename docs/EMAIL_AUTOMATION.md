# Stakeholder Email Automation

This build queues follow‑up emails as JSON drafts (no automatic sending by default).

## API
POST `/api/notify/email`
```
{
  "run_id": "run-20250101-120000",
  "to": ["security@company.com"],
  "subject": "Kaison Sentinel Findings Summary",
  "body": "Summary..."
}
```

Queued emails are written to `outputs/emails/`. If reports are plaintext, the report bundle is attached automatically.
