# Errors happen. Handle the ones you expect, let the rest crash loudly.

# %% try / except
try:
    print(10 / 0)
except ZeroDivisionError:
    print("cannot divide by zero")

# %% Several errors, else, finally
def parse_age(text):
    try:
        age = int(text)
    except ValueError:
        print(f"{text!r} is not a number")
        return None
    except TypeError:
        print("need text, got something else")
        return None
    else:
        print("parsed fine")          # runs only if no error
        return age
    finally:
        print("always runs")          # cleanup goes here


print(parse_age("42"))
print(parse_age("abc"))
print(parse_age(None))

# %% Get the error object
try:
    {"a": 1}["b"]
except KeyError as error:
    print("missing key:", error)

try:
    [1, 2][5]
except (IndexError, KeyError) as error:
    print(type(error).__name__, error)

# %% Raise your own errors
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError("not enough money")
    return balance - amount


try:
    withdraw(100, 500)
except ValueError as error:
    print(error)

# %% Custom exception classes
class PaymentError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


try:
    raise PaymentError("card declined", code=402)
except PaymentError as error:
    print(error, error.code)

# %% Chain errors (keep the original cause)
try:
    try:
        int("x")
    except ValueError as inner:
        raise RuntimeError("config is broken") from inner
except RuntimeError as outer:
    print(outer, "| caused by:", repr(outer.__cause__))

# %% Re-raise after logging
try:
    try:
        1 / 0
    except ZeroDivisionError:
        print("logging the problem")
        raise                        # pass the same error upward
except ZeroDivisionError:
    print("caught again higher up")

# %% Common built-in errors
for code in ["int('x')", "[][0]", "{}['k']", "None.upper()", "undefined_name", "'a' + 1", "open('nope.txt')"]:
    try:
        eval(code)
    except Exception as error:
        print(f"{code:18} -> {type(error).__name__}")

# %% Retry pattern (you will write this for APIs)
attempts = 0


def flaky():
    global attempts
    attempts += 1
    if attempts < 3:
        raise ConnectionError("network blip")
    return "ok"


for attempt in range(5):
    try:
        print(flaky(), "after", attempts, "tries")
        break
    except ConnectionError as error:
        print("retrying:", error)

# %% assert: a sanity check for yourself
x = 5
assert x > 0, "x must be positive"
