# Program Scope Cache

This folder stores downloaded scope and policy pages for public bug bounty programs.

To fetch and refresh scopes:

```bash
KAI_ALLOW_NETWORK=1 python3 scripts/fetch_program_guidelines.py --allow-network
```

Output layout:

```
data/programs/scopes/<program-id>/
  scope.html
  scope.txt
  policy.html
  policy.txt
  meta.json
```

Notes:
- This cache is for *program rules and scope only*.
- Always respect the program’s live scope page and safe‑harbor guidelines.
