# Real-world FastAPI: auth with dependencies, custom errors, middleware, background tasks.

import threading
import time

import httpx
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()
API_KEYS = {"key-asha": "asha", "key-ben": "ben"}
audit_log: list[str] = []


# %% Dependencies: reusable pieces injected into endpoints
def current_user(x_api_key: str = Header(default="")):
    user = API_KEYS.get(x_api_key)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid or missing API key")
    return user


def pagination(page: int = 1, size: int = 10):
    if size > 50:
        raise HTTPException(status_code=400, detail="size is at most 50")
    return {"offset": (page - 1) * size, "limit": size}


@app.get("/me")
def me(user: str = Depends(current_user)):
    return {"user": user}


@app.get("/items")
def items(user: str = Depends(current_user), page: dict = Depends(pagination)):
    return {"user": user, **page}


# %% Custom exceptions with their own response
class QuotaExceeded(Exception):
    def __init__(self, user):
        self.user = user


@app.exception_handler(QuotaExceeded)
async def quota_handler(request: Request, error: QuotaExceeded):
    return JSONResponse(status_code=429, content={"error": f"{error.user} used up the quota"})


@app.get("/expensive")
def expensive(user: str = Depends(current_user)):
    if user == "ben":
        raise QuotaExceeded(user)
    return {"result": "done"}


# %% Middleware: runs around every request
@app.middleware("http")
async def timing(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - start) * 1000:.1f}"
    return response


# %% Background tasks: respond now, work later
def write_audit(user, action):
    audit_log.append(f"{user} did {action}")


@app.post("/actions")
def actions(background: BackgroundTasks, user: str = Depends(current_user)):
    background.add_task(write_audit, user, "action")
    return {"accepted": True}


# %% Run and try it
def serve(application, port):
    server = uvicorn.Server(uvicorn.Config(application, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    return server, thread


server, thread = serve(app, 8103)
BASE = "http://127.0.0.1:8103"
asha = {"X-API-Key": "key-asha"}
ben = {"X-API-Key": "key-ben"}

print(httpx.get(f"{BASE}/me").status_code, httpx.get(f"{BASE}/me").json())
print(httpx.get(f"{BASE}/me", headers=asha).json())
print(httpx.get(f"{BASE}/items", headers=asha, params={"page": 3, "size": 5}).json())
print(httpx.get(f"{BASE}/items", headers=asha, params={"size": 500}).json())
print(httpx.get(f"{BASE}/expensive", headers=ben).status_code, httpx.get(f"{BASE}/expensive", headers=ben).json())

response = httpx.get(f"{BASE}/me", headers=asha)
print(response.headers["x-process-time-ms"], "ms")

httpx.post(f"{BASE}/actions", headers=asha)
time.sleep(0.2)
print(audit_log)

# %% CORS (needed when a browser app on another domain calls your API)
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(CORSMiddleware, allow_origins=["https://myapp.com"], allow_methods=["*"], allow_headers=["*"])

server.should_exit = True
thread.join(timeout=5)
