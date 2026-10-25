# An LLM API is just an HTTP call: you send messages, you get text back.
#
# To run the real calls, set a key in your terminal BEFORE starting Python:
#     export OPENAI_API_KEY="your key"        (see .env.example)
# Without a key, everything below still runs and shows what the response looks like.

import os

import requests
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"            # change to any current model name from your provider
client = OpenAI(api_key=API_KEY) if API_KEY else None

# %% The request is a list of messages
messages = [
    {"role": "system", "content": "You are a helpful assistant. Answer in one sentence."},
    {"role": "user", "content": "What is a DataFrame?"},
]
print(messages)

# %% The real call
if client:
    response = client.chat.completions.create(model=MODEL, messages=messages)
    print(response.choices[0].message.content)
else:
    print("(no key set, skipping the real call)")

# %% What a response looks like (shape you must know)
sample = {
    "id": "chatcmpl-123",
    "model": MODEL,
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "A DataFrame is a table of rows and columns."},
            "finish_reason": "stop",           # stop | length (cut off) | tool_calls | content_filter
        }
    ],
    "usage": {"prompt_tokens": 28, "completion_tokens": 12, "total_tokens": 40},
}
print(sample["choices"][0]["message"]["content"])
print(sample["choices"][0]["finish_reason"], sample["usage"])

# %% Parameters you will use
params = {
    "temperature": 0.0,       # 0 = predictable, 1+ = creative and random
    "max_tokens": 200,        # hard limit on the answer length (cost control)
    "top_p": 1.0,             # alternative to temperature, change one not both
    "n": 1,                   # number of answers
    "stop": ["\n\n"],         # stop when this text appears
    "seed": 42,               # more repeatable output (best effort)
}
if client:
    response = client.chat.completions.create(model=MODEL, messages=messages, **params)
    print(response.choices[0].message.content)
    print(response.usage)

# %% Tokens: models read tokens, not words (about 4 characters or 3/4 of a word)
text = "Retrieval augmented generation lets models use your own documents."
print(len(text), "characters ~", len(text) // 4, "tokens")
# Prices are charged per million tokens, input and output priced separately.
# Longer prompts and longer answers cost more and respond slower.

# %% Same call with plain HTTP (the SDK is a thin wrapper around this)
if API_KEY:
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": messages},
        timeout=30,
    )
    print(r.status_code, r.json()["choices"][0]["message"]["content"])

# %% Rules for keys
# 1. Never hard-code a key in a file.
# 2. Never commit one to git. If you do, revoke it immediately.
# 3. Use one key per project so you can revoke it safely.
# 4. Set spending limits in the provider dashboard.
