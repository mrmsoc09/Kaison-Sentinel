# Bootstrap & Tool Health

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
