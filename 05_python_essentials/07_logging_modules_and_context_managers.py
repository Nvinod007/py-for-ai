# Logging instead of print, context managers, and splitting code into modules.
# Each line has a short comment saying WHAT it is.

import argparse  # argparse: reads command line arguments
import json as j  # "as j": gives the library a shorter nickname
import logging  # logging: prints messages with a level and time
import math  # math: maths functions like sqrt
import os  # os: talk to the operating system
import time  # time: clock and sleep tools
from collections import OrderedDict  # OrderedDict: a dict that remembers order
from contextlib import contextmanager, suppress  # contextlib: helpers for "with" blocks

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% logging levels
logging.basicConfig(  # basicConfig: one-time setup of how logs look
    level=logging.INFO,  # level: hide messages less important than INFO
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",  # format: layout of each line (time | level | name | message)
    force=True,  # force=True: replace any earlier setup
)
log = logging.getLogger("app")  # getLogger(name): gets a logger with that name
log.debug("hidden at INFO level")  # debug: lowest level, hidden here
log.info("started")  # info: normal event
log.warning("disk almost full")  # warning: something might go wrong
log.error("could not save")  # error: something went wrong
log.info("user %s paid %.2f", "asha", 49.9)        # %s = put text here, %.2f = number with 2 decimals; lazy formatting

# %% Log an exception with its traceback
try:  # try: run code that might fail
    1 / 0  # impossible, raises an error
except ZeroDivisionError:  # except: runs if that error happened
    log.exception("math failed")                   # exception(): logs an error plus the traceback (where it failed)

# %% Context managers: setup and cleanup around a block
class Timer:  # class: a blueprint; this one works with "with"
    def __enter__(self):  # __enter__: runs when the with-block starts
        self.start = time.perf_counter()  # perf_counter(): precise clock in seconds
        return self  # return: sends a value back (it becomes "as" name)

    def __exit__(self, exc_type, exc, tb):  # __exit__: runs when the with-block ends (even after an error)
        self.elapsed = time.perf_counter() - self.start  # time passed
        print(f"took {self.elapsed:.4f}s")  # print: shows text; f-string puts values in; :.4f = 4 decimals
        return False                               # do not hide errors


with Timer():  # with: runs __enter__ first and __exit__ at the end
    sum(range(1_000_000))  # sum(): adds numbers; range(n): 0..n-1; 1_000_000 = one million


@contextmanager  # decorator: turns the generator below into a "with" helper
def announce(label):
    print("start", label)
    try:
        yield  # yield: pauses here while the with-block body runs
    finally:  # finally: always runs, even after an error
        print("end", label)


with announce("job"):
    print("working")

# %% Modules: every .py file is a module (imports live at the top of the file)
print(math.sqrt(16), j.dumps([1]), OrderedDict(a=1))  # sqrt: square root; dumps: Python -> JSON text; a=1 = name=value argument
print(__name__)                                    # __name__: this file's name; "__main__" when run directly


def main():  # def: makes a function
    print("running as a script")


if __name__ == "__main__":                         # if: runs block when test is True; runs only when executed directly
    main()

# %% Environment variables and secrets
api_key = os.environ.get("OPENAI_API_KEY")  # os.environ.get(name): reads an environment variable, or None if missing
print("key set" if api_key else "no key set (this is fine for now)")  # "A if test else B": picks A or B
# Never put keys in code or git. Keep them in environment variables or a
# local .env file that is listed in .gitignore. Share only .env.example.

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Ignore specific errors
with suppress(FileNotFoundError):  # suppress(Error): silently ignores that error inside the block
    open("missing.txt")  # open(path): opens a file (it doesn't exist, so it fails)
print("kept going")

# %% Packages and imports in a real project
# project/
#   pyproject.toml
#   src/myapp/__init__.py
#   src/myapp/utils.py     ->  from myapp.utils import clean_text
#   src/myapp/main.py
# Keep imports at the top of each file, one library per line.

# %% Command line arguments
parser = argparse.ArgumentParser()  # ArgumentParser(): object that reads command line options
parser.add_argument("--name", default="world")  # add_argument: declares an option; default = value if not given
parser.add_argument("--times", type=int, default=1)  # type=int: convert the input to a whole number
args = parser.parse_args([])                       # parse_args(list): reads options; [] so it runs in a notebook
print(f"hello {args.name}" * args.times)  # text * number repeats the text
