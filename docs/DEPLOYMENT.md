# Deployment

## Local (single host)
```
docker compose up --build
```

## Full stack (pgvector)
```
docker compose -f docker-compose.full.yml up --build
```

## Kubernetes (minimal)
```
kubectl apply -f k8s/pgvector.yaml
kubectl apply -f k8s/kaison-deployment.yaml
```
