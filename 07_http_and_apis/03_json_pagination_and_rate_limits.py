# Real APIs return JSON in pages and tell you to slow down. Handle both.
# Each line has a short comment saying WHAT it is.

import json  # json: convert between Python data and JSON text
import threading  # threading: run code in the background
import time  # time: clock and sleep tools
from http.server import BaseHTTPRequestHandler, HTTPServer  # http.server: tools to build a tiny web server
from urllib.parse import parse_qs, urlparse  # urlparse: splits a URL into parts; parse_qs: turns ?a=1&b=2 into a dict

import pandas as pd  # pandas (nickname pd): tables of data
import requests  # requests: library for calling web APIs

ITEMS = [{"id": i, "name": f"item{i}", "price": i * 3.5} for i in range(1, 26)]  # [.. for ..]: list comprehension builds a list of dicts; range(1, 26) = 1..25; f-string puts i in text
hits = {"count": 0}  # dict used as a counter


class Handler(BaseHTTPRequestHandler):  # class(Parent): our server code
    def do_GET(self):  # def: makes a function; runs for every GET request
        url = urlparse(self.path)  # urlparse(text): splits the URL into path and query
        query = parse_qs(url.query)  # parse_qs: ?page=2 -> {"page": ["2"]}
        if url.path == "/items":  # if: runs block when True
            page = int(query.get("page", ["1"])[0])  # get(key, default): value or default; [0]: first item; int(x): text -> number
            size = 10
            chunk = ITEMS[(page - 1) * size : page * size]  # list[a:b]: slice = part of the list from a up to (not including) b
            body = {"data": chunk, "next_page": page + 1 if page * size < len(ITEMS) else None}  # "A if test else B": picks A or B; len(x): how many items; None = "nothing"
            self._send(200, body)  # 200 = OK
        elif url.path == "/limited":  # elif: "else if"
            hits["count"] += 1  # += : add 1
            if hits["count"] <= 2:
                self._send(429, {"error": "slow down"}, {"Retry-After": "1"})  # 429 = Too Many Requests; Retry-After: seconds to wait
            else:
                self._send(200, {"ok": True})
        else:
            self._send(404, {})  # 404 = Not Found

    def _send(self, status, body, headers=None):  # _name = internal helper; headers=None = optional
        self.send_response(status)  # sends the status code
        self.send_header("Content-Type", "application/json")  # adds one reply header
        for key, value in (headers or {}).items():  # for: repeats; "a or b": use b if a is empty; .items(): (key, value) pairs
            self.send_header(key, value)
        self.end_headers()  # finishes the header part
        self.wfile.write(json.dumps(body).encode())  # dumps(): Python -> JSON text; encode(): -> bytes; wfile.write: sends it

    def log_message(self, *args):  # *args: accept any arguments; silences logging
        pass  # pass: do nothing


server = HTTPServer(("127.0.0.1", 8767), Handler)  # creates the server on this computer, port 8767
threading.Thread(target=server.serve_forever, daemon=True).start()  # runs the server in the background; daemon=True: stops with the script
BASE = "http://127.0.0.1:8767"

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% One page
page1 = requests.get(f"{BASE}/items", params={"page": 1}).json()  # requests.get(url): asks a server; params=dict: adds ?page=1; json(): reply -> Python
print(len(page1["data"]), page1["next_page"])  # print(x): shows x

# %% Loop through every page
all_items, page = [], 1  # two variables at once: empty list and 1
while page:  # while: repeats as long as page is not 0/None
    body = requests.get(f"{BASE}/items", params={"page": page}).json()
    all_items.extend(body["data"])  # extend(list): adds every item of that list
    page = body["next_page"]  # becomes None on the last page, which ends the loop
print(len(all_items))

# %% JSON into pandas
df = pd.DataFrame(all_items)  # DataFrame(list of dicts): makes a table
print(df.head(), df["price"].sum())  # head(): first 5 rows; df["col"]: one column; sum(): total

# %% Rate limit: obey Retry-After
for attempt in range(5):  # range(5): 0..4, so at most 5 tries
    r = requests.get(f"{BASE}/limited")
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 1))  # headers.get(name, default): header value or 1; int(): -> number
        print(f"rate limited, waiting {wait}s")
        time.sleep(wait)  # sleep(s): pauses s seconds
        continue  # continue: jump to the next loop round
    print("success:", r.json())
    break  # break: leave the loop


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Nested JSON
nested = [  # data with dicts inside dicts
    {"id": 1, "user": {"name": "Asha", "address": {"city": "Pune"}}, "tags": ["a", "b"]},
    {"id": 2, "user": {"name": "Ben", "address": {"city": "Delhi"}}, "tags": []},
]
print(pd.json_normalize(nested))                         # json_normalize: flattens nested data into columns
print(pd.json_normalize(nested, sep="_")[["user_name", "user_address_city"]])  # sep="_": joins nested names with _; [[..]]: pick these columns
print(nested[0]["user"]["address"].get("zip", "no zip"))   # dict.get(key, default): safe lookup, no error if missing

# %% Stop the server
server.shutdown()  # shutdown(): stops the server
