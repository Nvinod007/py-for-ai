# Tool calling: the model does not run code. It ASKS you to run a function,
# you run it, then you send the result back. This loop is the base of every agent.

import json
import os

from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None


# %% Your real Python functions
def get_weather(city):
    data = {"pune": "31C sunny", "paris": "17C rain"}
    return data.get(city.lower(), "unknown city")


def add(a, b):
    return a + b


FUNCTIONS = {"get_weather": get_weather, "add": add}

# %% Describe the tools to the model (JSON schema)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
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
print([t["function"]["name"] for t in TOOLS])


# %% A stand-in model that behaves like the real API
def fake_model(messages):
    last = messages[-1]
    if last["role"] == "user":
        return {"role": "assistant", "content": None, "tool_calls": [
            {"id": "call_1", "function": {"name": "get_weather", "arguments": '{"city": "Pune"}'}}
        ]}
    if last["role"] == "tool":
        return {"role": "assistant", "content": f"The weather in Pune is {last['content']}."}


# %% The tool loop (identical for real and fake models)
def run_tools(messages, model_call, max_steps=5):
    for step in range(max_steps):
        reply = model_call(messages)
        messages.append(reply)
        if not reply.get("tool_calls"):
            return reply["content"]                       # final answer
        for call in reply["tool_calls"]:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"])
            try:
                result = FUNCTIONS[name](**args)
            except Exception as error:
                result = f"tool error: {error}"           # tell the model, do not crash
            print(f"step {step}: {name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": str(result)})
    return "stopped: too many steps"


print(run_tools([{"role": "user", "content": "What's the weather in Pune?"}], fake_model))


# %% The same loop with the real API
def real_model(messages):
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    message = response.choices[0].message
    reply = {"role": "assistant", "content": message.content}
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
