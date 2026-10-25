# Tool calling: the model does not run code. It ASKS you to run a function,
# you run it, then you send the result back. This loop is the base of every agent.
# Each line has a short comment saying WHAT it is.

import json
import os

from openai import OpenAI

# os.environ.get(NAME): reads a setting from your terminal; gives None if it is not set.
API_KEY = os.environ.get("OPENAI_API_KEY")
# MODEL = the name of the AI model to use.
MODEL = "gpt-4o-mini"
# OpenAI(api_key=...): creates the object we use to talk to the API; None if there is no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Your real Python functions
# A normal Python function the AI can ask us to run.
def get_weather(city):
    data = {"pune": "31C sunny", "paris": "17C rain"}
    # dict.get(key, default): look up a key, or return the default if missing; lower(): lowercase.
    return data.get(city.lower(), "unknown city")


def add(a, b):
    return a + b


# FUNCTIONS: maps a tool name (text) to the real function so we can run it by name.
FUNCTIONS = {"get_weather": get_weather, "add": add}

# %% Describe the tools to the model (JSON schema)
# TOOLS: menu of tools described for the AI; it reads this to decide what to call.
TOOLS = [
    {
        # type 'function': this tool is a function.
        "type": "function",
        "function": {
            # name: what the AI uses to call it; description: when to use it.
            "name": "get_weather",
            "description": "Get current weather for a city.",
            # parameters: the inputs it takes, written as a JSON schema (types and which are required).
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                # required: inputs the AI must give.
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
            },
        },
    },
]
# List comprehension: collect each tool's name.
print([t["function"]["name"] for t in TOOLS])

# %% A stand-in model that behaves like the real API
# fake_model: pretends to be the AI; asks for a tool first, then answers using the tool result.
def fake_model(messages):
    # messages[-1]: the latest message.
    last = messages[-1]
    if last["role"] == "user":
        # tool_calls: the AI's request to run a tool; arguments is JSON text.
        return {"role": "assistant", "content": None, "tool_calls": [
            {"id": "call_1", "function": {"name": "get_weather", "arguments": '{"city": "Pune"}'}}
        ]}
    if last["role"] == "tool":
        return {"role": "assistant", "content": f"The weather in Pune is {last['content']}."}

# %% The tool loop (identical for real and fake models)
# run_tools: the loop: ask AI, run any requested tool, send result back; max_steps stops endless loops.
def run_tools(messages, model_call, max_steps=5):
    for step in range(max_steps):
        # Call the model (real or fake) with the conversation so far.
        reply = model_call(messages)
        # append: add the AI's reply to the conversation.
        messages.append(reply)
        # reply.get('tool_calls'): None/empty if the AI wants no tool, so it is the final answer.
        if not reply.get("tool_calls"):
            return reply["content"]                       # final answer
        for call in reply["tool_calls"]:
            name = call["function"]["name"]
            # json.loads: turn the JSON text arguments into a dict.
            args = json.loads(call["function"]["arguments"])
            try:
                # FUNCTIONS[name]: find the function; (**args): pass the dict as named inputs.
                result = FUNCTIONS[name](**args)
            except Exception as error:
                result = f"tool error: {error}"           # tell the model, do not crash
            print(f"step {step}: {name}({args}) -> {result}")
            # role tool: carries the result back; tool_call_id says which request it answers.
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": str(result)})
    return "stopped: too many steps"


# Start with one user message and the fake model.
print(run_tools([{"role": "user", "content": "What's the weather in Pune?"}], fake_model))

# %% The same loop with the real API
# real_model: same job as fake_model but calls the real API.
def real_model(messages):
    # tools=TOOLS: tells the AI which tools it may ask for.
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    # choices[0].message: the AI's reply object.
    message = response.choices[0].message
    reply = {"role": "assistant", "content": message.content}
    # tool_calls: the tools the AI wants run (None if none).
    if message.tool_calls:
        reply["tool_calls"] = [
            {"id": c.id, "type": "function", "function": {"name": c.function.name, "arguments": c.function.arguments}}
            for c in message.tool_calls
        ]
    return reply


if client:
    print(run_tools([{"role": "user", "content": "What is 12.5 + 7.5, and the weather in Paris?"}], real_model))

# %% Safety rules for tools
# 1. The model can call anything you list, so list only what is safe.
# 2. Validate every argument. Treat model output as untrusted user input.
# 3. Ask a human before dangerous actions (delete, pay, send email).
# 4. Always cap the number of loop steps.
# 5. Return errors as text so the model can recover.

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# (nothing rare here, everything above is core)
