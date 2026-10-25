# HTTP = how programs talk over the network. Every web API uses it.
# To work offline, this file starts a tiny local server and calls it.

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, headers=None):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path.startswith("/hello"):
            self._send(200, {"message": "hello", "path": self.path})
        elif self.path == "/items":
            self._send(200, [{"id": 1, "name": "pen"}, {"id": 2, "name": "book"}])
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(size) or b"{}")
        self._send(201, {"created": body})

    def do_DELETE(self):
        self._send(200, {"deleted": self.path})

    def log_message(self, *args):      # keep the terminal quiet
        pass


server = HTTPServer(("127.0.0.1", 8765), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8765"

# %% GET
response = requests.get(f"{BASE}/hello")
print(response.status_code)           # 200 = OK
print(response.json())                # parse the JSON body
print(response.text)                  # raw text
print(response.headers["Content-Type"])
print(response.ok, response.url, response.elapsed.total_seconds() < 5)

# %% Query parameters (?name=asha&page=2)
response = requests.get(f"{BASE}/hello", params={"name": "asha", "page": 2})
print(response.url)

# %% POST with JSON
response = requests.post(f"{BASE}/items", json={"name": "lamp", "price": 20})
print(response.status_code, response.json())

# %% Other methods
print(requests.delete(f"{BASE}/items/1").json())
# requests.put(url, json=...)   replace a whole item
# requests.patch(url, json=...) change part of an item

# %% Status codes you must know
for path in ["/hello", "/missing"]:
    r = requests.get(BASE + path)
    print(path, r.status_code, r.reason)
# 200 OK | 201 Created | 204 No Content
# 400 Bad Request | 401 Unauthorized | 403 Forbidden | 404 Not Found | 422 Invalid | 429 Too Many Requests
# 500 Server Error | 502/503 server down or busy

# %% Check for errors
r = requests.get(f"{BASE}/missing")
try:
    r.raise_for_status()
except requests.HTTPError as error:
    print("HTTP error:", error)

# %% Real public API (needs internet)
try:
    github = requests.get("https://api.github.com", timeout=5)
    print(github.status_code, list(github.json())[:3])
except requests.RequestException as error:
    print("no internet or blocked:", type(error).__name__)

server.shutdown()
