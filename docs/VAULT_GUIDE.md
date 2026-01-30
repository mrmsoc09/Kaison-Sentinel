# Vault Guide (OSINT)

## Providers registry
- File: `config/vault/providers.json`
- Each provider lists auth type and docs link.

## Add keys (CLI)
```
export KAI_ENCRYPTION_KEY="your-strong-key"
python3 -m kai11.vault_cli --add-key source.shodan --value "<key>"
```

## Add keys (UI)
- Use the **Key Vault (OSINT)** panel to add keys.

## List providers and keys
```
python3 -m kai11.vault_cli --list-providers
python3 -m kai11.vault_cli --list-keys
```
