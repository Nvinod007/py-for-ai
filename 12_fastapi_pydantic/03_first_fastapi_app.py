# FastAPI: turn Python functions into web endpoints.
#
# Run it as a real server from the terminal:
#     cd 12_fastapi_pydantic
#     uv run uvicorn 03_first_fastapi_app:app --reload
# Then open http://127.0.0.1:8000/docs for automatic interactive docs.
#
# Below, we also start the server in the background so the cells run on their own.
# Each line has a short comment saying WHAT it is.

# threading: run code in the background.
import threading
# time: sleep() pauses; other clock helpers.
import time

# httpx: a library to send web requests (GET, POST) from Python.
import httpx
# uvicorn: the server program that runs a FastAPI app.
import uvicorn
# FastAPI: the class that creates your web app.
from fastapi import FastAPI

# app: your web application; title and version show up in the docs.
app = FastAPI(title="My first API", version="0.1.0")


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Endpoints
# @app.get(path): the function below answers GET requests at that URL path.
@app.get("/")
# Returned dict is sent back as JSON automatically.
def home():
    return {"message": "hello"}


# {user_id} in the path is a path parameter; its value is passed to the function.
@app.get("/users/{user_id}")                      # path parameter
def get_user(user_id: int):                       # the type hint validates and converts
    return {"user_id": user_id}


# Function parameters not in the path become query parameters; ones with defaults are optional.
@app.get("/search")                               # query parameters: /search?q=pen&limit=5
def search(q: str, limit: int = 10, in_stock: bool = False):
    return {"q": q, "limit": limit, "in_stock": in_stock}


# A simple 'is the server alive' endpoint.
@app.get("/health")
def health():
    return {"status": "ok"}


# %% Helper to run the server in a background thread
# Starts the web server in a background thread so this script can also call it.
def serve(application, port):
    # uvicorn.Server/Config: uvicorn is the program that runs a FastAPI app; host/port = address, log_level='warning' = quiet.
    server = uvicorn.Server(uvicorn.Config(application, host="127.0.0.1", port=port, log_level="warning"))
    # Thread: runs server.run in the background; daemon=True means it dies when the script ends.
    thread = threading.Thread(target=server.run, daemon=True)
    # start(): begins running the thread.
    thread.start()
    # Wait (sleeping 0.05s each time) until the server is ready.
    while not server.started:
        time.sleep(0.05)
    return server, thread


# Asks the server to stop; thread.join(timeout=5) waits up to 5 seconds for it to finish.
def stop(server, thread):
    server.should_exit = True
    thread.join(timeout=5)


# %% Try it
# Start the server on port 8101 (a port is a numbered door on your computer).
server, thread = serve(app, 8101)
BASE = "http://127.0.0.1:8101"

# httpx.get(url).json(): send a GET request and read the JSON reply; params={...} adds ?key=value to the URL.
print(httpx.get(f"{BASE}/").json())
print(httpx.get(f"{BASE}/users/42").json())
print(httpx.get(f"{BASE}/search", params={"q": "pen", "limit": 3, "in_stock": True}).json())

# %% Automatic validation errors (422)
# 'abc' is not an int, so FastAPI replies 422 (invalid data); status_code is the reply number, 'detail' lists the problems.
response = httpx.get(f"{BASE}/users/abc")
print(response.status_code)
print(response.json()["detail"][0]["msg"])
response = httpx.get(f"{BASE}/search")           # q is required
print(response.status_code, response.json()["detail"][0]["loc"])


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Automatic docs and schema
# /openapi.json: automatic description of all endpoints; /docs: interactive page made from it.
openapi = httpx.get(f"{BASE}/openapi.json").json()
print(list(openapi["paths"]))
print(httpx.get(f"{BASE}/docs").status_code)     # open this URL in a browser when running for real

# %% Sync vs async endpoints
# def endpoint():        FastAPI runs it in a thread pool (fine for normal code)
# async def endpoint():  runs on the event loop, use with await for async libraries (httpx.AsyncClient, DBs)
# Never call slow blocking code (requests.get, time.sleep) inside async def.

# Shut the server down.
stop(server, thread)
