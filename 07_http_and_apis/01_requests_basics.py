# HTTP = how programs talk over the network. Every web API uses it.
# To work offline, this file starts a tiny local server and calls it.
# Each line has a short comment saying WHAT it is.

import json  # json: convert between Python data and JSON text
import threading  # threading: run code in the background
from http.server import BaseHTTPRequestHandler, HTTPServer  # http.server: tools to build a tiny web server

import requests  # requests: library for calling web APIs


class Handler(BaseHTTPRequestHandler):  # class(Parent): our server code, based on the ready-made handler
    def _send(self, status, body, headers=None):  # def: makes a function; _name = internal helper; headers=None = optional
        payload = json.dumps(body).encode()  # dumps(x): Python -> JSON text; encode(): text -> bytes (what the network sends)
        self.send_response(status)  # send_response(code): sends the status code (200 = OK)
        self.send_header("Content-Type", "application/json")  # send_header(name, value): adds one header (extra info about the reply)
        for key, value in (headers or {}).items():  # for: repeats; "a or b": use b if a is empty; .items(): (key, value) pairs
            self.send_header(key, value)
        self.end_headers()  # end_headers(): finishes the header part
        self.wfile.write(payload)  # wfile.write(bytes): sends the body to the client

    def do_GET(self):  # runs automatically for every GET request
        if self.path.startswith("/hello"):  # self.path: the URL path asked for; startswith(x): True if it begins with x
            self._send(200, {"message": "hello", "path": self.path})  # {..} = dict (key: value pairs)
        elif self.path == "/items":  # elif: "else if", checks another test
            self._send(200, [{"id": 1, "name": "pen"}, {"id": 2, "name": "book"}])  # [..] = list
        else:  # else: runs when no test above matched
            self._send(404, {"error": "not found"})  # 404 = Not Found

    def do_POST(self):  # runs automatically for every POST request (sending data)
        size = int(self.headers.get("Content-Length", 0))  # headers.get(name, default): value or default; int(x): text -> whole number
        body = json.loads(self.rfile.read(size) or b"{}")  # rfile.read(n): reads n bytes sent by the client; loads(): JSON text -> Python; b"{}" = bytes for empty JSON
        self._send(201, {"created": body})  # 201 = Created

    def do_DELETE(self):  # runs automatically for every DELETE request
        self._send(200, {"deleted": self.path})

    def log_message(self, *args):      # *args: accept any arguments; keep the terminal quiet
        pass  # pass: do nothing


server = HTTPServer(("127.0.0.1", 8765), Handler)  # HTTPServer((address, port), handler): creates the server; 127.0.0.1 = this computer
threading.Thread(target=server.serve_forever, daemon=True).start()  # Thread(target=f): runs f in the background; daemon=True: stops when the script ends; start(): begins it
BASE = "http://127.0.0.1:8765"  # base URL we will call

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% GET
response = requests.get(f"{BASE}/hello")  # requests.get(url): asks a server for data; f"..{x}": f-string puts values in text
print(response.status_code)           # print(x): shows x; 200 = OK
print(response.json())                # json(): parse the JSON body into Python
print(response.text)                  # raw text
print(response.headers["Content-Type"])  # headers: dict of reply headers
print(response.ok, response.url, response.elapsed.total_seconds() < 5)  # ok: True if status < 400; url: final URL; elapsed: time taken

# %% Query parameters (?name=asha&page=2)
response = requests.get(f"{BASE}/hello", params={"name": "asha", "page": 2})  # params=dict: adds ?key=value to the URL
print(response.url)

# %% POST with JSON
response = requests.post(f"{BASE}/items", json={"name": "lamp", "price": 20})  # requests.post(url): sends data; json=dict: sends it as JSON
print(response.status_code, response.json())

# %% Status codes you must know
for path in ["/hello", "/missing"]:  # for: repeats for each item in the list
    r = requests.get(BASE + path)  # + joins two texts
    print(path, r.status_code, r.reason)  # reason: short text for the status code
# 200 OK | 201 Created | 204 No Content
# 400 Bad Request | 401 Unauthorized | 403 Forbidden | 404 Not Found | 422 Invalid | 429 Too Many Requests
# 500 Server Error | 502/503 server down or busy

# %% Check for errors
r = requests.get(f"{BASE}/missing")
try:  # try: run code that might fail
    r.raise_for_status()  # raise_for_status(): throws an error if the status is 4xx/5xx
except requests.HTTPError as error:  # except: catches that error type; "as error" names it
    print("HTTP error:", error)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Other methods
print(requests.delete(f"{BASE}/items/1").json())  # requests.delete(url): asks the server to remove something
# requests.put(url, json=...)   replace a whole item
# requests.patch(url, json=...) change part of an item

# %% Real public API (needs internet)
try:
    github = requests.get("https://api.github.com", timeout=5)  # timeout=5: give up after 5 seconds
    print(github.status_code, list(github.json())[:3])  # list(dict): its keys; [:3]: first three
except requests.RequestException as error:  # RequestException: parent of all requests errors
    print("no internet or blocked:", type(error).__name__)  # type(x): kind of thing x is; __name__: its name


# %% Stop the server
server.shutdown()  # shutdown(): stops the server
