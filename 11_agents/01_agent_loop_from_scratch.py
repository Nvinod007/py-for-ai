# An agent = an LLM in a loop that can use tools.
#     think -> choose a tool -> run it -> read the result -> think again -> answer
# No framework needed. A scripted "fake model" stands in for the LLM so this runs offline.
# Each line has a short comment saying WHAT it is.

# json: read/write JSON text (a text format for dicts and lists).
import json
# re: regular expressions, a mini-language for matching text patterns.
import re

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Tools: plain Python functions
# def: defines a function; this tool does math on a text expression.
def calculator(expression: str) -> str:
    # re.fullmatch(pattern, text): True only if the WHOLE text matches the pattern.
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "error: only numbers and + - * / ( ) allowed"
    # eval(text, globals): runs text as Python code; {'__builtins__': {}} removes built-in functions for safety. str() turns the result into text.
    return str(eval(expression, {"__builtins__": {}}))        # restricted input only


# dict: pairs of key -> value, here a tiny fake knowledge base.
KNOWLEDGE = {
    "population of india": "about 1.43 billion",
    "capital of france": "Paris",
    "python creator": "Guido van Rossum",
}


# dict.get(key, default): returns the value, or the default if key is missing. .lower() makes lowercase, .strip() trims spaces.
def lookup(query: str) -> str:
    return KNOWLEDGE.get(query.lower().strip(), "no result found")


# Registry: tool name (text the model says) -> the function to call.
TOOLS = {"calculator": calculator, "lookup": lookup}


# %% The "model": returns either a tool request or a final answer as JSON.
# A real LLM does this decision for you. Here it follows a script to show the loop.
# A pretend LLM: reads the messages and returns what a real model might say.
def fake_llm(messages):
    task = messages[0]["content"].lower()
    # List comprehension: builds a list of tool results from the messages.
    observations = [m["content"] for m in messages if m["role"] == "tool"]
    # json.dumps(dict): turns a dict into JSON text, like a model's reply.
    if "capital of france" in task and not observations:
        return json.dumps({"action": "lookup", "input": "capital of france"})
    if "capital of france" in task and observations:
        return json.dumps({"final": f"The capital of France is {observations[-1]}."})
    if "12 * (3 + 4)" in task and not observations:
        return json.dumps({"action": "calculator", "input": "12 * (3 + 4)"})
    if "12 * (3 + 4)" in task and observations:
        return json.dumps({"final": f"The answer is {observations[-1]}."})
    return json.dumps({"final": "I am not sure how to do that."})


# %% The agent loop
# The agent loop; max_steps stops endless loops, verbose=True prints each step.
def run_agent(task, llm=fake_llm, max_steps=5, verbose=True):
    messages = [{"role": "user", "content": task}]
    # range(1, n+1): counts 1..n, one number per loop turn.
    for step in range(1, max_steps + 1):
        # json.loads(text): turns JSON text back into a dict.
        decision = json.loads(llm(messages))
        # list.append(x): adds x to the end of the list (the chat history).
        messages.append({"role": "assistant", "content": json.dumps(decision)})
        if "final" in decision:
            if verbose:
                print(f"step {step}: FINAL -> {decision['final']}")
            return decision["final"]
        # Look up the function by name; None if the model asked for an unknown tool.
        tool = TOOLS.get(decision["action"])
        result = tool(decision["input"]) if tool else f"error: unknown tool {decision['action']}"
        if verbose:
            print(f"step {step}: {decision['action']}({decision['input']!r}) -> {result}")
        messages.append({"role": "tool", "content": result})
    return "stopped: step limit reached"


# %% Try it
# Call the agent with a task; it prints each step.
run_agent("What is the capital of France?")
run_agent("Compute 12 * (3 + 4)")
run_agent("Sing me a song")

# %% What makes it an agent (not just a chatbot)
# 1. It decides WHICH tool to call and WHEN to stop (the model chooses, not your code).
# 2. Results of tools go back into the conversation (observations).
# 3. A loop continues until done or a limit is hit.


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Swap in a real model
# In 09_llm_apis/04_tool_calling.py the same loop uses the OpenAI tool-calling API.
# Everything else (tools, loop, limits) stays the same.
