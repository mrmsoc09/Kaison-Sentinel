# Program Scope Cache

This folder stores downloaded scope and policy pages for public bug bounty programs.

To fetch and refresh scopes:

```bash
python3 scripts/fetch_program_guidelines.py
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
