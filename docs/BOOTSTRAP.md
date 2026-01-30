# Bootstrap & Tool Health

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Generate a local tool health report
```
python3 scripts/bootstrap_tools.py
```

## View health report
```
python3 -m kai11.health_cli
```

## Include version checks
```
python3 -m kai11.health_cli --check-version
```

The report is written to `outputs/tool_health.json`.
