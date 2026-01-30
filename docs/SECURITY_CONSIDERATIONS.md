# Security Considerations

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

- Default deny for network and active scanning.
- HiL required for execute and reporting.
- Evidence and screen recording required for validated findings.
- API auth optional but supported; rate limiting enabled by default.
- Encryption supported for runs and reports; plaintext requires `KAI_ALLOW_PLAINTEXT=1`.
