FROM python:3.12-slim

# uv installs dependencies quickly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Dependencies first: this layer is cached until pyproject.toml changes
COPY pyproject.toml ./
RUN uv pip install --system --no-cache -r pyproject.toml

# Code last: changes often
COPY main.py ./

# Do not run as root
RUN useradd --create-home app
USER app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
