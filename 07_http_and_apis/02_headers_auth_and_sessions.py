# Headers, API keys, tokens, cookies, and Sessions.

import base64
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get("Authorization", "")
        if self.path == "/whoami":
            if auth == "Bearer secret-token":
                status, body = 200, {"user": "asha", "agent": self.headers.get("User-Agent")}
            else:
                status, body = 401, {"error": "missing or bad token"}
        elif self.path == "/basic":
            expected = "Basic " + base64.b64encode(b"asha:pw").decode()
            status, body = (200, {"ok": True}) if auth == expected else (401, {"error": "bad login"})
        elif self.path == "/cookie":
            status, body = 200, {"cookie": self.headers.get("Cookie")}
        else:
            status, body = 404, {}
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        if self.path == "/login":
            self.send_header("Set-Cookie", "sid=abc123")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 8766), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8766"

# %% No token -> 401
print(requests.get(f"{BASE}/whoami").status_code)

# %% Bearer token (the most common style, used by OpenAI, GitHub, and others)
headers = {"Authorization": "Bearer secret-token", "User-Agent": "my-app/1.0"}
print(requests.get(f"{BASE}/whoami", headers=headers).json())

# %% Basic auth (username + password)
print(requests.get(f"{BASE}/basic", auth=("asha", "pw")).json())

# %% API key in a header or in the URL
# requests.get(url, headers={"X-API-Key": key})
# requests.get(url, params={"api_key": key})        # less safe, keys end up in logs

# %% Sessions: reuse settings and connections
session = requests.Session()
session.headers.update(headers)
print(session.get(f"{BASE}/whoami").json())          # headers sent automatically
print(session.get(f"{BASE}/whoami").json())          # connection reused (faster)

# %% Cookies
session.cookies.set("sid", "abc123")
print(session.get(f"{BASE}/cookie").json())

# %% Where do keys come from? Environment variables, never source code
# import os
# key = os.environ["MY_API_KEY"]        # fails loudly when missing, which is good
# headers = {"Authorization": f"Bearer {key}"}

# %% Common headers
# Content-Type: application/json      what you send
# Accept: application/json            what you want back
# User-Agent: my-app/1.0              who you are
# Authorization: Bearer <token>       who you are, proven
# X-Request-ID: <id>                  trace one request across services

server.shutdown()
