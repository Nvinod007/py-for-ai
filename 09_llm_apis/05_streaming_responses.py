# Streaming: show words as they are generated, so users do not stare at a blank screen.

import os
import time

from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None


# %% A generator that behaves like a stream
def fake_stream(text):
    for word in text.split():
        time.sleep(0.05)
        yield word + " "


# %% Consume a stream
answer = ""
for piece in fake_stream("Streaming sends small pieces as soon as they are ready."):
    print(piece, end="", flush=True)
    answer += piece
print("\nfull text:", answer.strip())

# %% Real streaming
if client:
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Explain pandas in two sentences."}],
        stream=True,
    )
    full = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            print(delta, end="", flush=True)
            full += delta
    print()

# %% Measure what users feel
def measure(stream):
    start = time.perf_counter()
    first = None
    count = 0
    for _ in stream:
        count += 1
        if first is None:
            first = time.perf_counter() - start
    total = time.perf_counter() - start
    return first, total, count


first, total, count = measure(fake_stream("one two three four five six seven eight"))
print(f"time to first token {first:.2f}s, total {total:.2f}s, pieces {count}")

# %% Web apps send streams with Server-Sent Events (see folder 12, 06_llm_endpoint)
def sse(chunks):
    for chunk in chunks:
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"


print("".join(sse(["Hel", "lo"])))

# %% Tips
# - Stream for chat UIs. Do not stream when you need to parse complete JSON.
# - Handle cancellation: stop reading when the user leaves.
# - Tool calls also stream in pieces, collect them before running.
