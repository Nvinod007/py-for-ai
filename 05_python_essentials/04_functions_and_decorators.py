# Functions in depth, then decorators (used everywhere in FastAPI and agents).

import functools
import time

# %% Arguments
def greet(name, greeting="Hello", *, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"


print(greet("Asha"))
print(greet("Asha", "Hi"))
print(greet("Asha", punctuation="?"))          # keyword-only argument


def total(*numbers, **options):
    print("numbers:", numbers, "options:", options)
    return sum(numbers)


print(total(1, 2, 3, round=True))
values = [1, 2]
settings = {"round": False}
print(total(*values, **settings))               # unpack into arguments

# %% Never use a mutable default
def bad(item, bucket=[]):
    bucket.append(item)
    return bucket


print(bad(1), bad(2))                           # shared list, surprise


def good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print(good(1), good(2))

# %% Functions are objects
def shout(text):
    return text.upper()


operations = {"shout": shout, "len": len}
print(operations["shout"]("hi"), operations["len"]("hello"))
print(sorted(["bb", "a", "ccc"], key=lambda s: -len(s)))


def apply_twice(func, value):
    return func(func(value))


print(apply_twice(lambda x: x * 2, 3))

# %% Closures
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply


double = make_multiplier(2)
print(double(5))

# %% A decorator wraps a function
def timer(func):
    @functools.wraps(func)                      # keeps name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper


@timer
def slow_sum(n):
    """Add numbers."""
    return sum(range(n))


print(slow_sum(1_000_000), slow_sum.__name__)

# %% Decorator with its own arguments
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    print(f"attempt {attempt} failed: {error}")
            raise RuntimeError("all attempts failed")
        return wrapper
    return decorator


calls = {"n": 0}


@retry(times=3)
def unstable():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("boom")
    return "worked"


print(unstable())

# %% Built-in helpers
@functools.lru_cache(maxsize=None)              # remember results
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(60), fib.cache_info().hits > 0)
add_five = functools.partial(lambda a, b: a + b, 5)
print(add_five(10))

# %% Type hints (documentation that tools can check)
def average(values: list[float]) -> float:
    return sum(values) / len(values)


print(average([1, 2, 3]), average.__annotations__)

# %% Docstrings and help
def area(width, height):
    """Return the area of a rectangle."""
    return width * height


print(area.__doc__)
