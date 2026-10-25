# Logging instead of print, context managers, and splitting code into modules.

import argparse
import json as j
import logging
import math
import os
import time
from collections import OrderedDict
from contextlib import contextmanager, suppress

# %% logging levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    force=True,
)
log = logging.getLogger("app")
log.debug("hidden at INFO level")
log.info("started")
log.warning("disk almost full")
log.error("could not save")
log.info("user %s paid %.2f", "asha", 49.9)        # lazy formatting

# %% Log an exception with its traceback
try:
    1 / 0
except ZeroDivisionError:
    log.exception("math failed")                   # includes traceback

# %% Context managers: setup and cleanup around a block
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"took {self.elapsed:.4f}s")
        return False                               # do not hide errors


with Timer():
    sum(range(1_000_000))


@contextmanager
def announce(label):
    print("start", label)
    try:
        yield
    finally:
        print("end", label)


with announce("job"):
    print("working")

# %% Ignore specific errors
with suppress(FileNotFoundError):
    open("missing.txt")
print("kept going")

# %% Modules: every .py file is a module (imports live at the top of the file)
print(math.sqrt(16), j.dumps([1]), OrderedDict(a=1))
print(__name__)                                    # "__main__" when run directly


def main():
    print("running as a script")


if __name__ == "__main__":                         # runs only when executed directly
    main()

# %% Packages and imports in a real project
# project/
#   pyproject.toml
#   src/myapp/__init__.py
#   src/myapp/utils.py     ->  from myapp.utils import clean_text
#   src/myapp/main.py
# Keep imports at the top of each file, one library per line.

# %% Environment variables and secrets
api_key = os.environ.get("OPENAI_API_KEY")
print("key set" if api_key else "no key set (this is fine for now)")
# Never put keys in code or git. Keep them in environment variables or a
# local .env file that is listed in .gitignore. Share only .env.example.

# %% Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--name", default="world")
parser.add_argument("--times", type=int, default=1)
args = parser.parse_args([])                       # [] so it runs in a notebook
print(f"hello {args.name}" * args.times)
