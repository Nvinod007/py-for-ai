# 01 Docker concepts and commands

"It works on my machine" is the problem. Docker packages your app, Python version, and libraries into one box that runs the same everywhere.

## Words

| Term | Meaning |
|---|---|
| **Image** | A read-only package (the recipe result). Built from a Dockerfile. |
| **Container** | A running copy of an image (an isolated process). |
| **Dockerfile** | Text instructions to build an image. |
| **Registry** | Where images are stored (Docker Hub, GitHub Container Registry, AWS ECR). |
| **Volume** | Storage that survives when a container is deleted. |
| **Port mapping** | Connect a port on your computer to a port in the container. |

Image : container is like class : object.

## Everyday commands

```bash
docker --version
docker pull python:3.12-slim              # download an image
docker run --rm python:3.12-slim python -c "print('hi from a container')"

docker build -t my-api .                  # build an image from ./Dockerfile
docker run --rm -p 8000:8000 my-api       # run it, open http://localhost:8000
docker run -d --name api -p 8000:8000 my-api   # run in the background
docker logs -f api                        # follow the logs
docker exec -it api sh                    # open a shell inside it
docker stop api && docker rm api          # stop and delete it

docker ps                                 # running containers
docker ps -a                              # all containers
docker images                             # local images
docker rmi my-api                         # delete an image
docker system prune                       # clean up unused things
```

## Pass settings and secrets

```bash
docker run --rm -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY" my-api
docker run --rm --env-file .env my-api    # a local env file (never commit it)
```

Never write keys into the Dockerfile, because they stay inside the image layers.

## Keep data

```bash
docker run --rm -v "$PWD/data:/app/data" my-api      # share a local folder
docker volume create dbdata
docker run -v dbdata:/var/lib/postgresql/data postgres:16
```

## Run a database in one line

```bash
docker run -d --name pg -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:16
docker exec -it pg psql -U postgres
```

## Practice

1. Run `docker run --rm python:3.12-slim python -c "import sys; print(sys.version)"`.
2. Build the example in `05_example_app/` (see `02_dockerfile_for_a_fastapi_app.md`).
3. Start Postgres in a container and connect with `psql`.
