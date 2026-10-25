# Real-world FastAPI: auth with dependencies, custom errors, middleware, background tasks.
# Each line has a short comment saying WHAT it is.

# threading: run code in the background.
import threading
# time: sleep() pauses; perf_counter() is a precise stopwatch.
import time

# httpx: sends web requests from Python.
import httpx
# uvicorn: runs the FastAPI app as a server.
import uvicorn
# BackgroundTasks: run work after replying; Depends: plug in a helper function; Header: read a request header; HTTPException: error reply; Request: the incoming request.
from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Request
# JSONResponse: build a JSON reply yourself.
from fastapi.responses import JSONResponse

# Create the app.
app = FastAPI()
# Fake key -> user table.
API_KEYS = {"key-asha": "asha", "key-ben": "ben"}
# A list where we note what happened.
audit_log: list[str] = []


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Dependencies: reusable pieces injected into endpoints
# A dependency: finds the user from the 'x-api-key' header. Header(default='') reads that request header.
def current_user(x_api_key: str = Header(default="")):
    user = API_KEYS.get(x_api_key)
    if user is None:
        # 401 = not logged in; stops and replies with this error.
        raise HTTPException(status_code=401, detail="invalid or missing API key")
    return user


# Dependency that turns page/size into offset/limit numbers.
def pagination(page: int = 1, size: int = 10):
    if size > 50:
        raise HTTPException(status_code=400, detail="size is at most 50")
    return {"offset": (page - 1) * size, "limit": size}


# @app.get: GET endpoint.
@app.get("/me")
# Depends(current_user): FastAPI runs current_user first and passes its result in.
def me(user: str = Depends(current_user)):
    return {"user": user}


@app.get("/items")
# Two dependencies at once; {**page} merges that dict into the reply.
def items(user: str = Depends(current_user), page: dict = Depends(pagination)):
    return {"user": user, **page}


# %% Custom exceptions with their own response
# Our own error type (a class based on Exception).
class QuotaExceeded(Exception):
    def __init__(self, user):
        self.user = user


# @app.exception_handler(Err): when that error is raised, run the function below to build the reply.
@app.exception_handler(QuotaExceeded)
# async def: an async function (can wait without blocking). 429 = too many requests.
async def quota_handler(request: Request, error: QuotaExceeded):
    return JSONResponse(status_code=429, content={"error": f"{error.user} used up the quota"})


@app.get("/expensive")
# Raises our custom error for the user 'ben'.
def expensive(user: str = Depends(current_user)):
    if user == "ben":
        raise QuotaExceeded(user)
    return {"result": "done"}


# %% Middleware: runs around every request
# @app.middleware('http'): code that wraps EVERY request.
@app.middleware("http")
# call_next(request) passes the request on and gives back the response; await waits for it.
async def timing(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    # Adds a header to the reply with the elapsed time in ms (:.1f = 1 decimal).
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - start) * 1000:.1f}"
    return response


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Background tasks: respond now, work later
# The slow job we run after replying.
def write_audit(user, action):
    audit_log.append(f"{user} did {action}")


# @app.post: POST endpoint.
@app.post("/actions")
# BackgroundTasks: FastAPI gives you this to schedule jobs; add_task(func, args) runs it after the reply is sent.
def actions(background: BackgroundTasks, user: str = Depends(current_user)):
    background.add_task(write_audit, user, "action")
    return {"accepted": True}


# %% Run and try it
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


server, thread = serve(app, 8103)
BASE = "http://127.0.0.1:8103"
# Request headers (key/value info sent with a request) carrying an API key.
asha = {"X-API-Key": "key-asha"}
ben = {"X-API-Key": "key-ben"}

# No key -> 401 error reply.
print(httpx.get(f"{BASE}/me").status_code, httpx.get(f"{BASE}/me").json())
# headers={...} sends headers; params={...} adds ?key=value.
print(httpx.get(f"{BASE}/me", headers=asha).json())
print(httpx.get(f"{BASE}/items", headers=asha, params={"page": 3, "size": 5}).json())
print(httpx.get(f"{BASE}/items", headers=asha, params={"size": 500}).json())
print(httpx.get(f"{BASE}/expensive", headers=ben).status_code, httpx.get(f"{BASE}/expensive", headers=ben).json())

response = httpx.get(f"{BASE}/me", headers=asha)
print(response.headers["x-process-time-ms"], "ms")

# POST triggers the background task.
httpx.post(f"{BASE}/actions", headers=asha)
# Pause so the background task can finish.
time.sleep(0.2)
print(audit_log)

# %% CORS (needed when a browser app on another domain calls your API)
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(CORSMiddleware, allow_origins=["https://myapp.com"], allow_methods=["*"], allow_headers=["*"])

# Stop the server and wait up to 5 seconds.
server.should_exit = True
thread.join(timeout=5)
