import os

from fastapi import FastAPI

app = FastAPI(title="Example API")


@app.get("/health")
def health():
    return {"status": "ok", "env": os.environ.get("APP_ENV", "local")}


@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
