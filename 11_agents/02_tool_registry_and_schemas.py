# Writing JSON schemas by hand is boring. Generate them from your Python functions.

import inspect
import json
from typing import Callable, get_type_hints

REGISTRY: dict[str, Callable] = {}
PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean", list: "array", dict: "object"}


# %% A decorator that registers a function as a tool
def tool(func):
    REGISTRY[func.__name__] = func
    return func


def schema_for(func):
    hints = get_type_hints(func)
    signature = inspect.signature(func)
    properties, required = {}, []
    for name, param in signature.parameters.items():
        properties[name] = {"type": PY_TO_JSON.get(hints.get(name, str), "string")}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (inspect.getdoc(func) or "").split("\n")[0],
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


# %% Define tools normally
@tool
def get_order_status(order_id: int) -> str:
    """Look up the delivery status of an order."""
    return {101: "shipped", 102: "processing"}.get(order_id, "not found")


@tool
def send_email(to: str, subject: str, urgent: bool = False) -> str:
    """Send an email to a customer."""
    return f"email queued to {to} (urgent={urgent})"


print(json.dumps([schema_for(f) for f in REGISTRY.values()], indent=2))


# %% Safe dispatch: validate before running
def call_tool(name, arguments):
    if name not in REGISTRY:
        return f"error: unknown tool '{name}'. Available: {list(REGISTRY)}"
    func = REGISTRY[name]
    hints = get_type_hints(func)
    signature = inspect.signature(func)
    try:
        bound = signature.bind(**arguments)
    except TypeError as error:
        return f"error: bad arguments: {error}"
    for key, value in bound.arguments.items():
        expected = hints.get(key)
        if expected in PY_TO_JSON and not isinstance(value, expected):
            return f"error: '{key}' must be {expected.__name__}, got {type(value).__name__}"
    return func(**bound.arguments)


print(call_tool("get_order_status", {"order_id": 101}))
print(call_tool("get_order_status", {"order_id": "101"}))
print(call_tool("get_order_status", {}))
print(call_tool("delete_everything", {}))
print(call_tool("send_email", {"to": "a@b.com", "subject": "Hi"}))

# %% Tool design tips (they matter more than the framework)
# - Clear name and one-line description: the model chooses tools from these.
# - Few, focused tools beat many overlapping ones.
# - Return short, readable text or small JSON, not huge dumps.
# - Return helpful errors ("order 999 not found, ids look like 101") so the model can recover.
# - Make risky tools require confirmation (see 05_guardrails_and_human_approval.py).
