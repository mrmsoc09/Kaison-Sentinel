# Deployment

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

## Local (single host)
```
docker compose up --build
```
Set env vars as needed:
- `KAI_ENCRYPTION_KEY` or `KAI_ALLOW_PLAINTEXT=1`
- `KAI_ALLOW_NETWORK=1` (only for active scans)

## Full stack (pgvector)
```
docker compose -f docker-compose.full.yml up --build
```

## Kubernetes (minimal)
```
kubectl apply -f k8s/pgvector.yaml
kubectl apply -f k8s/kaison-deployment.yaml
```
