# Production Runbook

## Startup
1) Ensure pgvector is running (if enabled)
2) Start Kaison Sentinel API/UI

## Rollback
- Revert container image to previous tag
- Restore `outputs/` from backup

## Backups
- Archive `outputs/` daily
- Snapshot pgvector volume weekly
