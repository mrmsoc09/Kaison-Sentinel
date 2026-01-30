# Execution Notes

- Execution is disabled by default. To enable networked checks:
  - set `KAI_ALLOW_NETWORK=1`
- Encrypted storage is required unless explicitly disabled:
  - set `KAI_ENCRYPTION_KEY="..."` or `KAI_ALLOW_PLAINTEXT=1`

The default modules in this build are safe, passive checks:
- OSINT: DNS resolution for allowlisted targets
- Vuln: HTTP HEAD probe for missing security headers
