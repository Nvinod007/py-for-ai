# An agent = an LLM in a loop that can use tools.
#     think -> choose a tool -> run it -> read the result -> think again -> answer
# No framework needed. A scripted "fake model" stands in for the LLM so this runs offline.

import json
import re

# %% Tools: plain Python functions
def calculator(expression: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "error: only numbers and + - * / ( ) allowed"
    return str(eval(expression, {"__builtins__": {}}))        # restricted input only


KNOWLEDGE = {
    "population of india": "about 1.43 billion",
    "capital of france": "Paris",
    "python creator": "Guido van Rossum",
}


def lookup(query: str) -> str:
    return KNOWLEDGE.get(query.lower().strip(), "no result found")


TOOLS = {"calculator": calculator, "lookup": lookup}


# %% The "model": returns either a tool request or a final answer as JSON.
# A real LLM does this decision for you. Here it follows a script to show the loop.
def fake_llm(messages):
    task = messages[0]["content"].lower()
    observations = [m["content"] for m in messages if m["role"] == "tool"]
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
def run_agent(task, llm=fake_llm, max_steps=5, verbose=True):
    messages = [{"role": "user", "content": task}]
    for step in range(1, max_steps + 1):
        decision = json.loads(llm(messages))
        messages.append({"role": "assistant", "content": json.dumps(decision)})
        if "final" in decision:
            if verbose:
                print(f"step {step}: FINAL -> {decision['final']}")
            return decision["final"]
        tool = TOOLS.get(decision["action"])
        result = tool(decision["input"]) if tool else f"error: unknown tool {decision['action']}"
        if verbose:
            print(f"step {step}: {decision['action']}({decision['input']!r}) -> {result}")
        messages.append({"role": "tool", "content": result})
    return "stopped: step limit reached"


# %% Try it
run_agent("What is the capital of France?")
run_agent("Compute 12 * (3 + 4)")
run_agent("Sing me a song")

# %% What makes it an agent (not just a chatbot)
# 1. It decides WHICH tool to call and WHEN to stop (the model chooses, not your code).
# 2. Results of tools go back into the conversation (observations).
# 3. A loop continues until done or a limit is hit.

# %% Swap in a real model
# In 09_llm_apis/04_tool_calling.py the same loop uses the OpenAI tool-calling API.
# Everything else (tools, loop, limits) stays the same.
