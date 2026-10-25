# Networks fail. Production code always uses timeouts and retries.
# Each line has a short comment saying WHAT it is.

import json  # json: convert between Python data and JSON text
import random  # random: random numbers
import threading  # threading: run code in the background
import time  # time: clock and sleep tools
from http.server import BaseHTTPRequestHandler, HTTPServer  # http.server: tools to build a tiny web server

import requests  # requests: library for calling web APIs
from requests.adapters import HTTPAdapter  # HTTPAdapter: plug-in that controls how requests connects (retries)
from urllib3.util.retry import Retry  # Retry: settings describing when/how to retry

counter = {"n": 0}  # dict used as a counter


class Handler(BaseHTTPRequestHandler):  # class(Parent): our server code
    def do_GET(self):  # def: makes a function; runs for every GET request
        if self.path == "/slow":  # self.path: URL path asked for; if: runs block when True
            time.sleep(2)  # sleep(s): pauses s seconds (a slow server)
            status, body = 200, {"ok": True}  # set two variables at once
        elif self.path == "/flaky":  # elif: "else if"
            counter["n"] += 1  # += : add 1
            status, body = (503, {"error": "busy"}) if counter["n"] < 3 else (200, {"ok": True})  # "A if test else B": fails twice, then works; 503 = server busy
        else:
            status, body = 200, {"ok": True}
        self.send_response(status)  # sends the status code
        self.send_header("Content-Type", "application/json")  # adds one reply header
        self.end_headers()  # finishes the header part
        self.wfile.write(json.dumps(body).encode())  # dumps(): Python -> JSON text; encode(): -> bytes; wfile.write: sends it

    def log_message(self, *args):  # *args: accept any arguments; silences logging
        pass  # pass: do nothing


server = HTTPServer(("127.0.0.1", 8768), Handler)  # creates the server on this computer, port 8768
threading.Thread(target=server.serve_forever, daemon=True).start()  # runs the server in the background; daemon=True: stops with the script
BASE = "http://127.0.0.1:8768"

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% ALWAYS set a timeout (requests has none by default)
try:  # try: run code that might fail
    requests.get(f"{BASE}/slow", timeout=0.5)  # requests.get(url): asks a server; timeout=0.5: give up after 0.5 seconds; f"..{x}": f-string
except requests.Timeout:  # except: runs if that error happened
    print("timed out")  # print(x): shows x
print(requests.get(f"{BASE}/ok", timeout=(3, 10)).json())     # timeout=(connect, read) seconds; json(): reply -> Python

# %% Different kinds of failure
for url in [f"{BASE}/ok", "http://127.0.0.1:1/nothing"]:  # for: repeats for each URL (second one has nothing listening)
    try:
        r = requests.get(url, timeout=1)
        r.raise_for_status()  # raise_for_status(): throws an error if the status is 4xx/5xx
        print("good")
    except requests.ConnectionError:  # could not reach the server
        print("cannot connect")
    except requests.Timeout:  # server took too long
        print("timeout")
    except requests.HTTPError as error:  # bad status code; "as error" names it
        print("bad status", error.response.status_code)

# %% Manual retry with exponential backoff and jitter
def get_with_retry(url, attempts=5, base_delay=0.2):  # def: makes a function; attempts=5: default value
    for attempt in range(attempts):  # range(n): 0..n-1
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (429, 500, 502, 503, 504):  # "in": True if the value is in the group
                raise requests.HTTPError(f"retryable {r.status_code}")  # raise: throws an error on purpose
            return r  # return: sends a value back and ends the function
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as error:  # (A, B, C): catch any of these
            if attempt == attempts - 1:  # last try: give up
                raise  # raise alone: pass the same error upward
            delay = base_delay * 2**attempt + random.uniform(0, 0.1)  # 2**n = 2 to the power n (wait doubles each time); uniform(a, b): random decimal between a and b (jitter)
            print(f"attempt {attempt + 1} failed ({error}); retry in {delay:.2f}s")  # :.2f = 2 decimals
            time.sleep(delay)  # sleep(s): pauses s seconds


counter["n"] = 0
print(get_with_retry(f"{BASE}/flaky").json())

# %% What to retry
# Retry:       timeouts, connection errors, 429, 500, 502, 503, 504
# Do not retry: 400, 401, 403, 404, 422 (your request is wrong, retrying will not help)
# Retry only safe or idempotent calls (GET, PUT, DELETE), be careful with POST

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Retries built into requests
counter["n"] = 0
session = requests.Session()  # Session(): object that remembers settings across requests
retry = Retry(total=4, backoff_factor=0.2, status_forcelist=[502, 503, 504])  # total: max retries; backoff_factor: wait grows each time; status_forcelist: statuses to retry on
session.mount("http://", HTTPAdapter(max_retries=retry))  # mount(prefix, adapter): use this retry rule for all http:// URLs
print(session.get(f"{BASE}/flaky", timeout=2).json())

# %% Streaming a big download
with requests.get(f"{BASE}/ok", stream=True, timeout=2) as r:  # with: auto-closes at the end; stream=True: don't download the whole body yet
    size = sum(len(chunk) for chunk in r.iter_content(chunk_size=1024))  # iter_content(chunk_size=n): gives the body in pieces of n bytes; "x for ..." generator expression; len(): size; sum(): total
print(size, "bytes")


# %% Stop the server
server.shutdown()  # shutdown(): stops the server
