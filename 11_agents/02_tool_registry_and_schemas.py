# Writing JSON schemas by hand is boring. Generate them from your Python functions.
# Each line has a short comment saying WHAT it is.

# inspect: lets code look at functions (names, parameters, docstrings).
import inspect
# json: converts dicts/lists to JSON text for printing or sending.
import json
# Callable = 'any function' type; get_type_hints(func) returns the type labels written on a function.
from typing import Callable, get_type_hints

# REGISTRY: dict mapping tool name -> function. The ': dict[str, Callable]' part is just a type label.
REGISTRY: dict[str, Callable] = {}
# Translates Python types to JSON-schema type names (str -> 'string', etc.).
PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean", list: "array", dict: "object"}


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A decorator that registers a function as a tool
# Decorator: a function that takes a function, saves it, and returns it unchanged. func.__name__ is the function's name as text.
def tool(func):
    REGISTRY[func.__name__] = func
    return func


# Builds the JSON description (schema) of a function that the model reads.
def schema_for(func):
    # get_type_hints: dict of parameter name -> declared type.
    hints = get_type_hints(func)
    # inspect.signature: the function's parameter list.
    signature = inspect.signature(func)
    properties, required = {}, []
    # signature.parameters.items(): each parameter with its name and details.
    for name, param in signature.parameters.items():
        # dict.get(key, default): safe lookup with a fallback to 'string'.
        properties[name] = {"type": PY_TO_JSON.get(hints.get(name, str), "string")}
        # inspect.Parameter.empty means the parameter has no default, so it is required.
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            # inspect.getdoc(func): the function's docstring; split('\n')[0] keeps only its first line.
            "description": (inspect.getdoc(func) or "").split("\n")[0],
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


# %% Define tools normally
# @tool: registers the function below in REGISTRY when Python defines it.
@tool
# """...""" docstring: the description the model will see. dict.get(key, 'not found') gives a fallback.
def get_order_status(order_id: int) -> str:
    """Look up the delivery status of an order."""
    return {101: "shipped", 102: "processing"}.get(order_id, "not found")


# Same decorator again for a second tool; 'urgent: bool = False' is a parameter with a default so it's optional.
@tool
def send_email(to: str, subject: str, urgent: bool = False) -> str:
    """Send an email to a customer."""
    return f"email queued to {to} (urgent={urgent})"


# json.dumps(obj, indent=2): converts to pretty JSON text with 2-space indents.
print(json.dumps([schema_for(f) for f in REGISTRY.values()], indent=2))


# %% Safe dispatch: validate before running
# Safely runs a tool by name: checks the name and arguments before calling.
def call_tool(name, arguments):
    if name not in REGISTRY:
        return f"error: unknown tool '{name}'. Available: {list(REGISTRY)}"
    func = REGISTRY[name]
    hints = get_type_hints(func)
    signature = inspect.signature(func)
    try:
        # signature.bind(**arguments): matches the dict to parameters; raises TypeError if they don't fit. ** unpacks a dict into named arguments.
        bound = signature.bind(**arguments)
    # except: runs only if the code above raised that error.
    except TypeError as error:
        return f"error: bad arguments: {error}"
    # isinstance(value, type): True if the value is of that type.
    for key, value in bound.arguments.items():
        expected = hints.get(key)
        if expected in PY_TO_JSON and not isinstance(value, expected):
            return f"error: '{key}' must be {expected.__name__}, got {type(value).__name__}"
    # Call the real function with the checked arguments.
    return func(**bound.arguments)


# Good call, wrong type, missing argument, unknown tool, missing required field: each shows a different error message.
print(call_tool("get_order_status", {"order_id": 101}))
print(call_tool("get_order_status", {"order_id": "101"}))
print(call_tool("get_order_status", {}))
print(call_tool("delete_everything", {}))
print(call_tool("send_email", {"to": "a@b.com", "subject": "Hi"}))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Tool design tips (they matter more than the framework)
# - Clear name and one-line description: the model chooses tools from these.
# - Few, focused tools beat many overlapping ones.
# - Return short, readable text or small JSON, not huge dumps.
# - Return helpful errors ("order 999 not found, ids look like 101") so the model can recover.
# - Make risky tools require confirmation (see 05_guardrails_and_human_approval.py).
