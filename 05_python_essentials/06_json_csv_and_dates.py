# JSON is the language of APIs. Also CSV, dates, and handy standard-library tools.
# Each line has a short comment saying WHAT it is.

import csv  # csv: read/write spreadsheet-like text files
import json  # json: convert between Python data and JSON text
import os  # os: talk to the operating system (environment variables)
import random  # random: random numbers and choices
import re  # re: regular expressions (pattern matching in text)
import sys  # sys: info about Python itself
import tempfile  # tempfile: temporary files/folders
from collections import Counter, defaultdict, deque, namedtuple  # collections: extra container types
from datetime import date, datetime, timedelta  # date/datetime: dates and times; timedelta: a length of time
from pathlib import Path  # Path: object for file/folder paths

work = Path(tempfile.mkdtemp())  # mkdtemp(): new empty temp folder

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% JSON <-> Python
data = {"name": "Asha", "age": 25, "skills": ["python", "sql"], "active": True, "boss": None}  # dict = key: value pairs; None = "nothing"
text = json.dumps(data)  # dumps(obj): Python -> JSON text ("dump string")
print(text)  # print(x): shows x
print(json.dumps(data, indent=2))  # indent=2: pretty print with 2-space indents
print(json.dumps(data, sort_keys=True, separators=(",", ":")))  # sort_keys=True: alphabetical keys; separators: compact punctuation
back = json.loads(text)  # loads(text): JSON text -> Python ("load string")
print(back["skills"][0], back["boss"], type(back))  # dict["key"] gets a value; [0] first item; type(x): kind of thing x is

# %% JSON files
(work / "d.json").write_text(json.dumps(data, indent=2))  # "/" joins paths; write_text(s): saves text to a file
with open(work / "d.json", encoding="utf-8") as f:  # with: auto-closes the file; open(path): opens it; encoding="utf-8" = normal text; "as f" names it
    print(json.load(f))  # load(file): reads JSON from a file object
with open(work / "out.json", "w", encoding="utf-8") as f:  # "w" = write (overwrite)
    json.dump(data, f, indent=2, ensure_ascii=False)  # dump(obj, file): writes JSON to a file; ensure_ascii=False keeps non-English letters

# %% CSV
rows = [{"name": "Asha", "age": 25}, {"name": "Ben", "age": 32}]  # list of dicts
with open(work / "p.csv", "w", newline="", encoding="utf-8") as f:  # newline="": stops blank lines being added in CSV files
    writer = csv.DictWriter(f, fieldnames=["name", "age"])  # DictWriter: writes dicts as CSV rows; fieldnames = column order
    writer.writeheader()  # writes the column names line
    writer.writerows(rows)  # writes every dict as a row
with open(work / "p.csv", newline="", encoding="utf-8") as f:  # no mode = read
    for row in csv.DictReader(f):  # for: loops; DictReader: gives each row as a dict using the header names
        print(row)

# %% Dates and times
today = date.today()  # today's date
now = datetime.now()  # current date and time
print(today.year >= 2026, now.hour in range(24))  # .year/.hour: parts of the date; "in": True if value is inside the range
d = datetime(2024, 3, 15, 14, 30)  # datetime(year, month, day, hour, minute)
print(d.strftime("%d %b %Y, %H:%M"), d.isoformat())  # strftime(format): date -> text (%d day, %b month name, %Y year, %H:%M time); isoformat(): standard text form
print(datetime.strptime("15/03/2024", "%d/%m/%Y"))  # strptime(text, format): text -> date
print(datetime.fromisoformat("2024-03-15T14:30:00"))  # fromisoformat(text): standard text -> date
print(d + timedelta(days=30, hours=2), d - datetime(2024, 1, 1))  # timedelta: a length of time; date + time = later date; date - date = time between
print(d.weekday(), d.date(), d.time())  # weekday(): Monday=0 ... Sunday=6; date()/time(): just that part

# %% random, os, sys basics
random.seed(1)  # seed(n): makes random numbers repeatable
print(random.randint(1, 6), random.choice(["a", "b"]), random.sample(range(10), 3))  # randint(a, b): whole number a..b; choice(list): one random item; sample(items, 3): 3 different items
print(os.environ.get("HOME") is not None, sys.version_info[:2], sys.platform)  # os.environ: environment variables; .get(name): value or None; version_info[:2]: Python major.minor; platform: your OS name
print(os.environ.get("MY_SETTING", "default"))     # get(name, default): uses default if missing; how you read settings and API keys

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Things JSON cannot store by default
try:  # try: run code that might fail
    json.dumps({"when": datetime(2024, 1, 1)})  # datetime(y, m, d): a date-time value
except TypeError as error:  # except: catches that error type; "as error" names it
    print(error)
print(json.dumps({"when": datetime(2024, 1, 1)}, default=str))  # default=str: for unknown types, use str() to make text

# %% Bad JSON
try:
    json.loads("{'single': 'quotes'}")  # JSON needs double quotes, so this fails
except json.JSONDecodeError as error:
    print("bad JSON:", error.msg)  # error.msg: short reason text

# %% JSON lines (one JSON per line, common for logs and datasets)
lines = "\n".join(json.dumps({"id": i}) for i in range(3))  # "sep".join(items): glues strings with sep; "x for ..." is a generator expression; \n = new line; range(3) = 0..2
print([json.loads(line)["id"] for line in lines.splitlines()])  # [.. for ..]: list comprehension; splitlines(): text -> list of lines

# %% collections
print(Counter("mississippi").most_common(2))  # Counter: counts items; most_common(2): top 2 with counts
groups = defaultdict(list)  # defaultdict(list): dict that auto-creates an empty list for new keys
for word in ["apple", "avocado", "banana"]:  # for: repeats for each item
    groups[word[0]].append(word)  # word[0] = first letter; append(x): adds x to the list
print(dict(groups))  # dict(x): turns it into a normal dict
queue = deque([1, 2, 3], maxlen=3)  # deque: list that is fast at both ends; maxlen=3 drops the oldest when full
queue.append(4)
print(queue)
Point = namedtuple("Point", ["x", "y"])  # namedtuple: a tuple (fixed group) whose parts have names
print(Point(1, 2), Point(1, 2).x)

# %% Regular expressions
text = "Call 555-1234 or 555-9876. Mail a@b.com"
print(re.findall(r"\d{3}-\d{4}", text))  # findall(pattern, text): all matches as a list; r"..." = raw text; \d = a digit; {3} = exactly 3 times
print(re.search(r"(\w+)@(\w+)\.com", text).groups())  # search: first match; \w+ = one or more letters/digits; () capture a part; groups(): the captured parts
print(re.sub(r"\d", "#", text))  # sub(pattern, new, text): replaces every match
print(re.split(r"[ ,.]+", "a, b. c"))  # split(pattern, text): cuts text at matches; [ ,.] = any of those characters
print(bool(re.fullmatch(r"\d+", "123")))  # fullmatch: whole text must match; bool(x): True/False
