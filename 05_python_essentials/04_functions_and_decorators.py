# Functions in depth, then decorators (used everywhere in FastAPI and agents).
# Each line has a short comment saying WHAT it is.

import functools  # import: loads a library; functools has helpers for functions
import time  # time: clock and sleep tools

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Arguments
def greet(name, greeting="Hello", *, punctuation="!"):  # def: makes a function; greeting="Hello" = default value; "*," means arguments after it must be named
    return f"{greeting}, {name}{punctuation}"  # return: sends a value back; f"..{x}": f-string puts values inside text


print(greet("Asha"))  # print(x): shows x
print(greet("Asha", "Hi"))
print(greet("Asha", punctuation="?"))          # keyword-only argument: you must write name=value


def total(*numbers, **options):  # *numbers: collects extra values into a tuple; **options: collects name=value pairs into a dict
    print("numbers:", numbers, "options:", options)
    return sum(numbers)  # sum(x): adds all the numbers


print(total(1, 2, 3, round=True))
values = [1, 2]  # a list
settings = {"round": False}  # a dict (key: value pairs)
print(total(*values, **settings))               # *list spreads items as arguments; **dict spreads as name=value

# %% Never use a mutable default
def bad(item, bucket=[]):  # the default [] is made once and shared by every call (a trap)
    bucket.append(item)  # list.append(x): adds x to the end
    return bucket


print(bad(1), bad(2))                           # shared list, surprise


def good(item, bucket=None):  # None = "nothing"; safe default
    if bucket is None:  # if: runs block when test is True; "is None" checks for nothing
        bucket = []  # make a fresh list each call
    bucket.append(item)
    return bucket


print(good(1), good(2))

# %% Functions are objects
def shout(text):
    return text.upper()  # upper(): makes text capital letters


operations = {"shout": shout, "len": len}  # functions can be stored in a dict; len(x) = how many items
print(operations["shout"]("hi"), operations["len"]("hello"))  # dict["key"] gets the function, then () calls it
print(sorted(["bb", "a", "ccc"], key=lambda s: -len(s)))  # sorted(list, key=f): sort using f's result; lambda: tiny one-line function; - flips to longest first


def apply_twice(func, value):  # func is a function passed in as an argument
    return func(func(value))


print(apply_twice(lambda x: x * 2, 3))

# %% A decorator wraps a function
def timer(func):  # a decorator: takes a function, returns a new wrapped one
    @functools.wraps(func)                      # wraps(func): keeps the original name and docstring
    def wrapper(*args, **kwargs):  # *args/**kwargs: accept any arguments and pass them along
        start = time.perf_counter()  # perf_counter(): precise clock in seconds
        result = func(*args, **kwargs)  # call the real function
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")  # __name__: function's name; :.4f = 4 decimal places
        return result
    return wrapper


@timer  # @decorator: applies timer to the function below
def slow_sum(n):
    """Add numbers."""  # docstring: description text of the function
    return sum(range(n))  # range(n): numbers 0..n-1


print(slow_sum(1_000_000), slow_sum.__name__)  # 1_000_000 = one million

# %% Type hints (documentation that tools can check)
def average(values: list[float]) -> float:  # "name: type" and "-> type" are hints for readers/tools; Python doesn't enforce them
    return sum(values) / len(values)  # / divides; len(x): how many items


print(average([1, 2, 3]), average.__annotations__)  # __annotations__: dict of the hints

# %% Docstrings and help
def area(width, height):
    """Return the area of a rectangle."""  # docstring: description text of the function
    return width * height


print(area.__doc__)  # __doc__: the docstring text

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Closures
def make_multiplier(factor):
    def multiply(x):  # a function inside a function
        return x * factor  # remembers factor from outside (a closure)
    return multiply  # returns the function itself, not its result


double = make_multiplier(2)
print(double(5))

# %% Decorator with its own arguments
def retry(times):  # outer function takes the decorator's settings
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):  # for: repeats; range(1, n): counts from 1
                try:  # try: run code that might fail
                    return func(*args, **kwargs)
                except Exception as error:  # except: catches errors; "as error" names it
                    print(f"attempt {attempt} failed: {error}")
            raise RuntimeError("all attempts failed")  # raise: throws an error on purpose
        return wrapper
    return decorator


calls = {"n": 0}


@retry(times=3)  # decorator with an argument
def unstable():
    calls["n"] += 1  # += : add 1
    if calls["n"] < 3:
        raise ConnectionError("boom")  # ConnectionError: built-in network error
    return "worked"


print(unstable())

# %% Built-in helpers
@functools.lru_cache(maxsize=None)              # lru_cache: remembers results so repeated calls are instant; maxsize=None = no limit
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)  # "A if test else B": picks A or B


print(fib(60), fib.cache_info().hits > 0)  # cache_info(): stats about the cache; hits = times it reused a result
add_five = functools.partial(lambda a, b: a + b, 5)  # partial(f, 5): a new function with the first argument fixed to 5
print(add_five(10))
