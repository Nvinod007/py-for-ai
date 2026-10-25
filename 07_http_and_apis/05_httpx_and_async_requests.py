# httpx: like requests, but also supports async. Most modern AI SDKs use it.

import asyncio
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.4)                               # a slow API
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"path": self.path}).encode())

    def log_message(self, *args):
        pass


class Server(ThreadingHTTPServer):
    request_queue_size = 64            # allow many connections at once


server = Server(("127.0.0.1", 8769), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8769"


def run(coro):
    # works inside interactive windows and plain scripts
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


# %% Sync usage looks like requests
response = httpx.get(f"{BASE}/one", timeout=5)
print(response.status_code, response.json())

with httpx.Client(base_url=BASE, timeout=5, headers={"X-App": "demo"}) as client:
    print(client.get("/two").json())

# %% Async: 8 calls at the same time
async def fetch_all():
    async with httpx.AsyncClient(base_url=BASE, timeout=5) as client:
        responses = await asyncio.gather(*(client.get(f"/item/{i}") for i in range(8)))
        return [r.json()["path"] for r in responses]


start = time.perf_counter()
print(run(fetch_all()))
print(f"8 calls took {time.perf_counter() - start:.1f}s (one by one would be 3.2s)")

# %% Limit how many requests run together
async def fetch_limited(limit=3):
    semaphore = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(base_url=BASE, timeout=5) as client:
        async def one(i):
            async with semaphore:
                return (await client.get(f"/n/{i}")).status_code
        return await asyncio.gather(*(one(i) for i in range(6)))


print(run(fetch_limited()))

# %% Errors and timeouts
try:
    httpx.get(f"{BASE}/slow", timeout=0.1)
except httpx.TimeoutException:
    print("timeout")
try:
    httpx.get("http://127.0.0.1:1/x", timeout=1)
except httpx.ConnectError:
    print("connect error")

# %% httpx vs requests
# requests: simplest, sync only
# httpx:    same style + async + HTTP/2 + better timeouts. Use it for new projects.

server.shutdown()
