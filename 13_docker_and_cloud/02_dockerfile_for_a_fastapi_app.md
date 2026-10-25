# 02 Dockerfile for a FastAPI app

The working example is in `05_example_app/`.

```text
05_example_app/
  main.py            the FastAPI app
  pyproject.toml     dependencies
  Dockerfile         build instructions
  .dockerignore      files to keep out of the image
  compose.yaml       run it with one command
```

## Build and run

```bash
cd 13_docker_and_cloud/05_example_app
docker build -t example-api .
docker run --rm -p 8000:8000 example-api
curl localhost:8000/health
```

## The Dockerfile, line by line

| Line | Why |
|---|---|
| `FROM python:3.12-slim` | Start from a small official Python image. |
| `COPY --from=ghcr.io/astral-sh/uv ...` | Get `uv` for fast dependency installs. |
| `WORKDIR /app` | Folder inside the container. |
| `COPY pyproject.toml ./` then install | Copy dependency files FIRST so Docker caches the install layer. |
| `COPY main.py ./` | Copy code last, because code changes most often. |
| `EXPOSE 8000` | Documents the port. |
| `USER app` | Do not run as root. |
| `CMD [...]` | The command that starts the server. `--host 0.0.0.0` is required so it is reachable from outside. |

## Rules for good images

1. **Order layers** from least to most often changed (dependencies before code).
2. **Use `.dockerignore`** to skip `.venv`, `.git`, `__pycache__`, `.env`, and data.
3. **Slim base images** (`-slim`) keep images small and safer.
4. **Pin versions** (`python:3.12-slim`, not `latest`).
5. **One process per container.**
6. **Never bake secrets** into the image. Pass them at run time.
7. **Health check** an endpoint (`/health`) so platforms know when you are ready.

## Common problems

| Symptom | Cause and fix |
|---|---|
| Cannot open the app in the browser | Server bound to `127.0.0.1`. Use `--host 0.0.0.0`. |
| `port is already allocated` | Another thing uses port 8000. Use `-p 8001:8000`. |
| Image is huge | Missing `.dockerignore`, or a heavy library like torch. |
| Rebuilds install everything every time | Code was copied before the dependency step. |
