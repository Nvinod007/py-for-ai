# Networks fail. Production code always uses timeouts and retries.

import json
import random
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

counter = {"n": 0}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/slow":
            time.sleep(2)
            status, body = 200, {"ok": True}
        elif self.path == "/flaky":
            counter["n"] += 1
            status, body = (503, {"error": "busy"}) if counter["n"] < 3 else (200, {"ok": True})
        else:
            status, body = 200, {"ok": True}
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 8768), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8768"

# %% ALWAYS set a timeout (requests has none by default)
try:
    requests.get(f"{BASE}/slow", timeout=0.5)
except requests.Timeout:
    print("timed out")
print(requests.get(f"{BASE}/ok", timeout=(3, 10)).json())     # (connect, read)

# %% Different kinds of failure
for url in [f"{BASE}/ok", "http://127.0.0.1:1/nothing"]:
    try:
        r = requests.get(url, timeout=1)
        r.raise_for_status()
        print("good")
    except requests.ConnectionError:
        print("cannot connect")
    except requests.Timeout:
        print("timeout")
    except requests.HTTPError as error:
        print("bad status", error.response.status_code)

# %% Manual retry with exponential backoff and jitter
def get_with_retry(url, attempts=5, base_delay=0.2):
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"retryable {r.status_code}")
            return r
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as error:
            if attempt == attempts - 1:
                raise
            delay = base_delay * 2**attempt + random.uniform(0, 0.1)
            print(f"attempt {attempt + 1} failed ({error}); retry in {delay:.2f}s")
            time.sleep(delay)


counter["n"] = 0
print(get_with_retry(f"{BASE}/flaky").json())

# %% Retries built into requests
counter["n"] = 0
session = requests.Session()
retry = Retry(total=4, backoff_factor=0.2, status_forcelist=[502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retry))
print(session.get(f"{BASE}/flaky", timeout=2).json())

# %% What to retry
# Retry:       timeouts, connection errors, 429, 500, 502, 503, 504
# Do not retry: 400, 401, 403, 404, 422 (your request is wrong, retrying will not help)
# Retry only safe or idempotent calls (GET, PUT, DELETE), be careful with POST

# %% Streaming a big download
with requests.get(f"{BASE}/ok", stream=True, timeout=2) as r:
    size = sum(len(chunk) for chunk in r.iter_content(chunk_size=1024))
print(size, "bytes")

server.shutdown()
