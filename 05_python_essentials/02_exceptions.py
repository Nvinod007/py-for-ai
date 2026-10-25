# Errors happen. Handle the ones you expect, let the rest crash loudly.
# Each line has a short comment saying WHAT it is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% try / except
try:  # try: run code that might fail
    print(10 / 0)  # 10 / 0 is impossible, so Python raises an error
except ZeroDivisionError:  # except: runs if that error type happened
    print("cannot divide by zero")

# %% Several errors, else, finally
def parse_age(text):  # def: makes a function named parse_age
    try:
        age = int(text)  # int(x): turns text like "42" into the number 42
    except ValueError:  # ValueError: right type, bad value (like "abc")
        print(f"{text!r} is not a number")  # f-string: puts values in text; !r shows the value with quotes
        return None  # return: sends a value back and ends the function; None = "nothing"
    except TypeError:  # TypeError: wrong type of thing (like None)
        print("need text, got something else")
        return None
    else:  # else: runs only if the try had no error
        print("parsed fine")          # runs only if no error
        return age
    finally:  # finally: runs no matter what
        print("always runs")          # cleanup goes here


print(parse_age("42"))
print(parse_age("abc"))
print(parse_age(None))

# %% Get the error object
try:
    {"a": 1}["b"]  # {...} = dict (key: value pairs); ["b"] looks up a key that is not there
except KeyError as error:  # KeyError: dict key not found; "as error" names the error object
    print("missing key:", error)

try:
    [1, 2][5]  # [..] = list; [5] asks for position 5 which doesn't exist
except (IndexError, KeyError) as error:  # (A, B): catch either error type
    print(type(error).__name__, error)  # type(x): what kind of thing x is; __name__: its name

# %% Raise your own errors
def withdraw(balance, amount):
    if amount <= 0:  # if: runs the block only when the test is True
        raise ValueError("amount must be positive")  # raise: stops and throws an error on purpose
    if amount > balance:
        raise ValueError("not enough money")
    return balance - amount


try:
    withdraw(100, 500)
except ValueError as error:
    print(error)

# %% Common built-in errors
for code in ["int('x')", "[][0]", "{}['k']", "None.upper()", "undefined_name", "'a' + 1", "open('nope.txt')"]:  # for: repeats for each text in the list
    try:
        eval(code)  # eval(text): runs text as Python code (only for demos, unsafe on real input)
    except Exception as error:  # Exception: catches almost any error
        print(f"{code:18} -> {type(error).__name__}")  # {code:18} = pad text to 18 characters wide

# %% Retry pattern (you will write this for APIs)
attempts = 0


def flaky():
    global attempts  # global: lets this function change the outside variable
    attempts += 1  # += : add 1
    if attempts < 3:
        raise ConnectionError("network blip")  # ConnectionError: built-in error for network failures
    return "ok"


for attempt in range(5):  # range(5): numbers 0 to 4
    try:
        print(flaky(), "after", attempts, "tries")
        break  # break: leaves the loop early
    except ConnectionError as error:
        print("retrying:", error)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Custom exception classes
class PaymentError(Exception):  # class(Exception): makes your own error type based on Exception
    def __init__(self, message, code):  # __init__: runs when the error is created
        super().__init__(message)  # super(): the parent class; sets up the normal message
        self.code = code  # self.code: extra data saved on the error


try:
    raise PaymentError("card declined", code=402)  # code=402: keyword argument (name=value)
except PaymentError as error:
    print(error, error.code)

# %% Chain errors (keep the original cause)
try:
    try:
        int("x")  # fails: "x" is not a number
    except ValueError as inner:
        raise RuntimeError("config is broken") from inner  # raise ... from x: new error that remembers x as the cause
except RuntimeError as outer:
    print(outer, "| caused by:", repr(outer.__cause__))  # repr(x): text showing x exactly; __cause__: the original error

# %% Re-raise after logging
try:
    try:
        1 / 0
    except ZeroDivisionError:
        print("logging the problem")
        raise                        # raise alone: pass the same error upward
except ZeroDivisionError:
    print("caught again higher up")

# %% assert: a sanity check for yourself
x = 5
assert x > 0, "x must be positive"  # assert test, msg: stops with msg if test is False
