# Headers, API keys, tokens, cookies, and Sessions.
# Each line has a short comment saying WHAT it is.

import base64  # base64: turns bytes into plain text letters
import json  # json: convert between Python data and JSON text
import threading  # threading: run code in the background
from http.server import BaseHTTPRequestHandler, HTTPServer  # http.server: tools to build a tiny web server

import requests  # requests: library for calling web APIs


class Handler(BaseHTTPRequestHandler):  # class(Parent): our server code, based on the ready-made handler
    def do_GET(self):  # def: makes a function; runs for every GET request
        auth = self.headers.get("Authorization", "")  # headers.get(name, default): header value or "" if missing
        if self.path == "/whoami":  # self.path: URL path asked for; if: runs block when True
            if auth == "Bearer secret-token":  # == : True if equal
                status, body = 200, {"user": "asha", "agent": self.headers.get("User-Agent")}  # "a, b = x, y": set two variables at once; {..} = dict
            else:  # else: runs when the test was False
                status, body = 401, {"error": "missing or bad token"}  # 401 = Unauthorized
        elif self.path == "/basic":  # elif: "else if"
            expected = "Basic " + base64.b64encode(b"asha:pw").decode()  # b"..." = bytes; b64encode: encode as base64; decode(): bytes -> text
            status, body = (200, {"ok": True}) if auth == expected else (401, {"error": "bad login"})  # "A if test else B": picks A or B
        elif self.path == "/cookie":
            status, body = 200, {"cookie": self.headers.get("Cookie")}
        else:
            status, body = 404, {}  # 404 = Not Found
        payload = json.dumps(body).encode()  # dumps(): Python -> JSON text; encode(): text -> bytes
        self.send_response(status)  # sends the status code
        self.send_header("Content-Type", "application/json")  # send_header(name, value): adds one reply header
        if self.path == "/login":
            self.send_header("Set-Cookie", "sid=abc123")  # Set-Cookie: tells the client to save a cookie
        self.end_headers()  # finishes the header part
        self.wfile.write(payload)  # wfile.write(bytes): sends the body

    def log_message(self, *args):  # *args: accept any arguments; silences logging
        pass  # pass: do nothing


server = HTTPServer(("127.0.0.1", 8766), Handler)  # creates the server on this computer, port 8766
threading.Thread(target=server.serve_forever, daemon=True).start()  # runs the server in the background; daemon=True: stops with the script
BASE = "http://127.0.0.1:8766"

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% No token -> 401
print(requests.get(f"{BASE}/whoami").status_code)  # print(x): shows x; requests.get(url): asks a server for data; f"..{x}": f-string; status_code: result number

# %% Bearer token (the most common style, used by OpenAI, GitHub, and others)
headers = {"Authorization": "Bearer secret-token", "User-Agent": "my-app/1.0"}  # dict of extra info sent with the request
print(requests.get(f"{BASE}/whoami", headers=headers).json())  # headers=dict: sends those headers; json(): parse the reply into Python

# %% Basic auth (username + password)
print(requests.get(f"{BASE}/basic", auth=("asha", "pw")).json())  # auth=(user, password): sends a login

# %% Sessions: reuse settings and connections
session = requests.Session()  # Session(): an object that remembers headers/cookies across requests
session.headers.update(headers)  # update(dict): adds those headers to every request
print(session.get(f"{BASE}/whoami").json())          # headers sent automatically
print(session.get(f"{BASE}/whoami").json())          # connection reused (faster)

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


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% API key in a header or in the URL
# requests.get(url, headers={"X-API-Key": key})
# requests.get(url, params={"api_key": key})        # less safe, keys end up in logs

# %% Cookies
session.cookies.set("sid", "abc123")  # cookies.set(name, value): saves a cookie to send each time
print(session.get(f"{BASE}/cookie").json())

# %% Stop the server
server.shutdown()  # shutdown(): stops the server
