# 03 Docker Compose and environments

Compose runs several containers together (API + database + cache) with one file.

## Start and stop

```bash
cd 13_docker_and_cloud/05_example_app
docker compose up --build         # build and run, Ctrl+C to stop
docker compose up -d              # in the background
docker compose logs -f api
docker compose ps
docker compose down               # stop and remove containers
docker compose down -v            # also delete volumes (data!)
```

## What `compose.yaml` does

- `api` is built from the local Dockerfile and maps port 8000.
- `db` is an official Postgres image with a named volume so data survives restarts.
- `depends_on` with a health check starts the API after the database is ready.
- The API reaches the database at host name `db` (service names are DNS names inside the compose network), not `localhost`.

## Settings per environment

| Environment | Where settings come from |
|---|---|
| Local | your shell, or a local env file that git ignores |
| CI | the CI platform's secret store |
| Production | the platform's secret manager (AWS Secrets Manager, Vercel/Render env settings, Kubernetes secrets) |

Code should read **only** environment variables (`os.environ`). Then the same image runs everywhere.

Share a `.env.example` with fake values so teammates know which names to set.

## 12-factor basics (the habits behind this)

1. Config in the environment, not in code.
2. Logs go to standard output (`print`, logging to console). The platform collects them.
3. Processes are stateless. Store data in a database or object storage.
4. Same image for dev, test, and production.
5. Fast start, graceful stop.

## Practice

1. Run `docker compose up --build` and call `http://localhost:8000/health`.
2. Add a `redis` service to `compose.yaml` and connect to it.
3. Change a setting by editing the `environment` section and restart.
