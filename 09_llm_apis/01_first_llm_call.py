# An LLM API is just an HTTP call: you send messages, you get text back.
#
# To run the real calls, set a key in your terminal BEFORE starting Python:
#     export OPENAI_API_KEY="your key"        (see .env.example)
# Without a key, everything below still runs and shows what the response looks like.
# Each line has a short comment saying WHAT it is.

import os

import requests
from openai import OpenAI

# os.environ.get(NAME): reads a setting from your terminal; gives None if it is not set.
API_KEY = os.environ.get("OPENAI_API_KEY")
# MODEL = the name of the AI model to use (a cheap, fast one).
MODEL = "gpt-4o-mini"            # change to any current model name from your provider
# OpenAI(api_key=...): creates the object we use to talk to the API; None if there is no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% The request is a list of messages
# messages: the conversation as a list; role says who speaks (system = rules for the AI, user = you), content is the text.
messages = [
    {"role": "system", "content": "You are a helpful assistant. Answer in one sentence."},
    {"role": "user", "content": "What is a DataFrame?"},
]
print(messages)

# %% The real call
if client:
    # client.chat.completions.create(...): sends the messages to the AI and returns its reply; model = which AI, messages = the conversation.
    response = client.chat.completions.create(model=MODEL, messages=messages)
    # choices[0].message.content: the answer text (choices is a list; we take the first).
    print(response.choices[0].message.content)
else:
    print("(no key set, skipping the real call)")

# %% What a response looks like (shape you must know)
# sample: a pretend response showing its shape; id = call id, model = who answered.
sample = {
    "id": "chatcmpl-123",
    "model": MODEL,
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "A DataFrame is a table of rows and columns."},
            # finish_reason: why the AI stopped (stop = done, length = ran out of tokens).
            "finish_reason": "stop",           # stop | length (cut off) | tool_calls | content_filter
        }
    ],
    # usage: how many tokens were used (prompt = what you sent, completion = what it wrote); you pay by tokens.
    "usage": {"prompt_tokens": 28, "completion_tokens": 12, "total_tokens": 40},
}
print(sample["choices"][0]["message"]["content"])
print(sample["choices"][0]["finish_reason"], sample["usage"])

# %% Parameters you will use
# params: extra settings passed to create(); ** later unpacks them as named arguments.
params = {
    "temperature": 0.0,       # 0 = predictable, 1+ = creative and random
    "max_tokens": 200,        # hard limit on the answer length (cost control)
    "top_p": 1.0,             # alternative to temperature, change one not both
    "n": 1,                   # number of answers
    "stop": ["\n\n"],         # stop when this text appears
    "seed": 42,               # more repeatable output (best effort)
}
if client:
    # **params: spread the dictionary into temperature=..., max_tokens=..., etc.
    response = client.chat.completions.create(model=MODEL, messages=messages, **params)
    print(response.choices[0].message.content)
    print(response.usage)

# %% Tokens: models read tokens, not words (about 4 characters or 3/4 of a word)
text = "Retrieval augmented generation lets models use your own documents."
# len(text) // 4: whole-number division, a rough token estimate (about 4 characters per token).
print(len(text), "characters ~", len(text) // 4, "tokens")
# Prices are charged per million tokens, input and output priced separately.
# Longer prompts and longer answers cost more and respond slower.

# %% Rules for keys
# 1. Never hard-code a key in a file.
# 2. Never commit one to git. If you do, revoke it immediately.
# 3. Use one key per project so you can revoke it safely.
# 4. Set spending limits in the provider dashboard.

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Same call with plain HTTP (the SDK is a thin wrapper around this)
if API_KEY:
    # requests.post(url, ...): sends data to a web address; url = the API, headers = login info (Bearer = your key), json = the request body, timeout = give up after 30 seconds.
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": messages},
        timeout=30,
    )
    # r.status_code: 200 means OK; r.json(): turns the reply text into a Python dictionary.
    print(r.status_code, r.json()["choices"][0]["message"]["content"])
