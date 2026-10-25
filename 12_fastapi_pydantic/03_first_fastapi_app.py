# FastAPI: turn Python functions into web endpoints.
#
# Run it as a real server from the terminal:
#     cd 12_fastapi_pydantic
#     uv run uvicorn 03_first_fastapi_app:app --reload
# Then open http://127.0.0.1:8000/docs for automatic interactive docs.
#
# Below, we also start the server in the background so the cells run on their own.

import threading
import time

import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="My first API", version="0.1.0")


# %% Endpoints
@app.get("/")
def home():
    return {"message": "hello"}


@app.get("/users/{user_id}")                      # path parameter
def get_user(user_id: int):                       # the type hint validates and converts
    return {"user_id": user_id}


@app.get("/search")                               # query parameters: /search?q=pen&limit=5
def search(q: str, limit: int = 10, in_stock: bool = False):
    return {"q": q, "limit": limit, "in_stock": in_stock}


@app.get("/health")
def health():
    return {"status": "ok"}


# %% Helper to run the server in a background thread
def serve(application, port):
    server = uvicorn.Server(uvicorn.Config(application, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    return server, thread


def stop(server, thread):
    server.should_exit = True
    thread.join(timeout=5)


# %% Try it
server, thread = serve(app, 8101)
BASE = "http://127.0.0.1:8101"

print(httpx.get(f"{BASE}/").json())
print(httpx.get(f"{BASE}/users/42").json())
print(httpx.get(f"{BASE}/search", params={"q": "pen", "limit": 3, "in_stock": True}).json())

# %% Automatic validation errors (422)
response = httpx.get(f"{BASE}/users/abc")
print(response.status_code)
print(response.json()["detail"][0]["msg"])
response = httpx.get(f"{BASE}/search")           # q is required
print(response.status_code, response.json()["detail"][0]["loc"])

# %% Automatic docs and schema
openapi = httpx.get(f"{BASE}/openapi.json").json()
print(list(openapi["paths"]))
print(httpx.get(f"{BASE}/docs").status_code)     # open this URL in a browser when running for real

# %% Sync vs async endpoints
# def endpoint():        FastAPI runs it in a thread pool (fine for normal code)
# async def endpoint():  runs on the event loop, use with await for async libraries (httpx.AsyncClient, DBs)
# Never call slow blocking code (requests.get, time.sleep) inside async def.

stop(server, thread)
