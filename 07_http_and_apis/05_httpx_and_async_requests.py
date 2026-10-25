# httpx: like requests, but also supports async. Most modern AI SDKs use it.
# Each line has a short comment saying WHAT it is.

import asyncio  # asyncio: Python's tool for running waiting jobs together
import json  # json: convert between Python data and JSON text
import threading  # threading: run code in the background
import time  # time: clock and sleep tools
from concurrent.futures import ThreadPoolExecutor  # ThreadPoolExecutor: runs functions in separate threads (workers)
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # ThreadingHTTPServer: web server that handles many requests at once

import httpx  # httpx: like requests, but with async support


class Handler(BaseHTTPRequestHandler):  # class(Parent): our server code
    def do_GET(self):  # def: makes a function; runs for every GET request
        time.sleep(0.4)                               # sleep(s): pauses s seconds; a slow API
        self.send_response(200)  # sends status code 200 = OK
        self.send_header("Content-Type", "application/json")  # adds one reply header
        self.end_headers()  # finishes the header part
        self.wfile.write(json.dumps({"path": self.path}).encode())  # dumps(): Python -> JSON text; encode(): -> bytes; wfile.write: sends it

    def log_message(self, *args):  # *args: accept any arguments; silences logging
        pass  # pass: do nothing


class Server(ThreadingHTTPServer):  # our server, based on ThreadingHTTPServer
    request_queue_size = 64            # setting: how many waiting connections are allowed at once


server = Server(("127.0.0.1", 8769), Handler)  # creates the server on this computer, port 8769
threading.Thread(target=server.serve_forever, daemon=True).start()  # runs the server in the background; daemon=True: stops with the script
BASE = "http://127.0.0.1:8769"


def run(coro):  # coro = an async function call waiting to be run
    # works inside interactive windows and plain scripts
    with ThreadPoolExecutor(max_workers=1) as pool:  # with: auto-cleans up at the end; max_workers=1: one helper thread
        return pool.submit(asyncio.run, coro).result()  # submit(f, x): runs f(x) in a thread; asyncio.run: runs an async function to the end; result(): waits for the answer

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Sync usage looks like requests
response = httpx.get(f"{BASE}/one", timeout=5)  # httpx.get(url): asks a server for data; timeout=5: give up after 5 seconds; f"..{x}": f-string
print(response.status_code, response.json())  # print(x): shows x; json(): reply -> Python

with httpx.Client(base_url=BASE, timeout=5, headers={"X-App": "demo"}) as client:  # Client(): reuses connections; base_url: start of every URL; headers: sent every time
    print(client.get("/two").json())

# %% Async: 8 calls at the same time
async def fetch_all():  # async def: a function that can pause while waiting
    async with httpx.AsyncClient(base_url=BASE, timeout=5) as client:  # async with: like with, for async things; AsyncClient: async version of Client
        responses = await asyncio.gather(*(client.get(f"/item/{i}") for i in range(8)))  # await: pause until done; gather(...): runs all together, results in order; *(...) spreads them as arguments
        return [r.json()["path"] for r in responses]  # [.. for ..]: list comprehension; return: sends the value back


start = time.perf_counter()  # perf_counter(): precise clock in seconds
print(run(fetch_all()))
print(f"8 calls took {time.perf_counter() - start:.1f}s (one by one would be 3.2s)")  # :.1f = 1 decimal

# %% Errors and timeouts
try:  # try: run code that might fail
    httpx.get(f"{BASE}/slow", timeout=0.1)  # server takes 0.4s, so this times out
except httpx.TimeoutException:  # except: runs if that error happened
    print("timeout")
try:
    httpx.get("http://127.0.0.1:1/x", timeout=1)  # nothing listens on port 1
except httpx.ConnectError:  # could not reach the server
    print("connect error")

# %% httpx vs requests
# requests: simplest, sync only
# httpx:    same style + async + HTTP/2 + better timeouts. Use it for new projects.


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Limit how many requests run together
async def fetch_limited(limit=3):  # limit=3: default value
    semaphore = asyncio.Semaphore(limit)  # Semaphore(n): allows at most n jobs at the same time
    async with httpx.AsyncClient(base_url=BASE, timeout=5) as client:
        async def one(i):  # a function inside a function
            async with semaphore:  # waits for a free slot
                return (await client.get(f"/n/{i}")).status_code
        return await asyncio.gather(*(one(i) for i in range(6)))  # range(6) = 0..5


print(run(fetch_limited()))

# %% Stop the server
server.shutdown()  # shutdown(): stops the server
