# JSON is the language of APIs. Also CSV, dates, and handy standard-library tools.

import csv
import json
import os
import random
import re
import sys
import tempfile
from collections import Counter, defaultdict, deque, namedtuple
from datetime import date, datetime, timedelta
from pathlib import Path

work = Path(tempfile.mkdtemp())

# %% JSON <-> Python
data = {"name": "Asha", "age": 25, "skills": ["python", "sql"], "active": True, "boss": None}
text = json.dumps(data)
print(text)
print(json.dumps(data, indent=2))
print(json.dumps(data, sort_keys=True, separators=(",", ":")))
back = json.loads(text)
print(back["skills"][0], back["boss"], type(back))

# %% JSON files
(work / "d.json").write_text(json.dumps(data, indent=2))
with open(work / "d.json", encoding="utf-8") as f:
    print(json.load(f))
with open(work / "out.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# %% Things JSON cannot store by default
try:
    json.dumps({"when": datetime(2024, 1, 1)})
except TypeError as error:
    print(error)
print(json.dumps({"when": datetime(2024, 1, 1)}, default=str))

# %% Bad JSON
try:
    json.loads("{'single': 'quotes'}")
except json.JSONDecodeError as error:
    print("bad JSON:", error.msg)

# %% JSON lines (one JSON per line, common for logs and datasets)
lines = "\n".join(json.dumps({"id": i}) for i in range(3))
print([json.loads(line)["id"] for line in lines.splitlines()])

# %% CSV
rows = [{"name": "Asha", "age": 25}, {"name": "Ben", "age": 32}]
with open(work / "p.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
with open(work / "p.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row)

# %% Dates and times
today = date.today()
now = datetime.now()
print(today.year >= 2026, now.hour in range(24))
d = datetime(2024, 3, 15, 14, 30)
print(d.strftime("%d %b %Y, %H:%M"), d.isoformat())
print(datetime.strptime("15/03/2024", "%d/%m/%Y"))
print(datetime.fromisoformat("2024-03-15T14:30:00"))
print(d + timedelta(days=30, hours=2), d - datetime(2024, 1, 1))
print(d.weekday(), d.date(), d.time())

# %% collections
print(Counter("mississippi").most_common(2))
groups = defaultdict(list)
for word in ["apple", "avocado", "banana"]:
    groups[word[0]].append(word)
print(dict(groups))
queue = deque([1, 2, 3], maxlen=3)
queue.append(4)
print(queue)
Point = namedtuple("Point", ["x", "y"])
print(Point(1, 2), Point(1, 2).x)

# %% Regular expressions
text = "Call 555-1234 or 555-9876. Mail a@b.com"
print(re.findall(r"\d{3}-\d{4}", text))
print(re.search(r"(\w+)@(\w+)\.com", text).groups())
print(re.sub(r"\d", "#", text))
print(re.split(r"[ ,.]+", "a, b. c"))
print(bool(re.fullmatch(r"\d+", "123")))

# %% random, os, sys basics
random.seed(1)
print(random.randint(1, 6), random.choice(["a", "b"]), random.sample(range(10), 3))
print(os.environ.get("HOME") is not None, sys.version_info[:2], sys.platform)
print(os.environ.get("MY_SETTING", "default"))     # how you read settings and API keys
