# Real APIs return JSON in pages and tell you to slow down. Handle both.

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests

ITEMS = [{"id": i, "name": f"item{i}", "price": i * 3.5} for i in range(1, 26)]
hits = {"count": 0}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        if url.path == "/items":
            page = int(query.get("page", ["1"])[0])
            size = 10
            chunk = ITEMS[(page - 1) * size : page * size]
            body = {"data": chunk, "next_page": page + 1 if page * size < len(ITEMS) else None}
            self._send(200, body)
        elif url.path == "/limited":
            hits["count"] += 1
            if hits["count"] <= 2:
                self._send(429, {"error": "slow down"}, {"Retry-After": "1"})
            else:
                self._send(200, {"ok": True})
        else:
            self._send(404, {})

    def _send(self, status, body, headers=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 8767), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8767"

# %% One page
page1 = requests.get(f"{BASE}/items", params={"page": 1}).json()
print(len(page1["data"]), page1["next_page"])

# %% Loop through every page
all_items, page = [], 1
while page:
    body = requests.get(f"{BASE}/items", params={"page": page}).json()
    all_items.extend(body["data"])
    page = body["next_page"]
print(len(all_items))

# %% JSON into pandas
df = pd.DataFrame(all_items)
print(df.head(), df["price"].sum())

# %% Nested JSON
nested = [
    {"id": 1, "user": {"name": "Asha", "address": {"city": "Pune"}}, "tags": ["a", "b"]},
    {"id": 2, "user": {"name": "Ben", "address": {"city": "Delhi"}}, "tags": []},
]
print(pd.json_normalize(nested))                         # flattens into columns
print(pd.json_normalize(nested, sep="_")[["user_name", "user_address_city"]])
print(nested[0]["user"]["address"].get("zip", "no zip"))   # safe lookup

# %% Rate limit: obey Retry-After
for attempt in range(5):
    r = requests.get(f"{BASE}/limited")
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 1))
        print(f"rate limited, waiting {wait}s")
        time.sleep(wait)
        continue
    print("success:", r.json())
    break

server.shutdown()
