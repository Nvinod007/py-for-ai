# Cost math, handling API errors, and the Anthropic (Claude) SDK.

import os
import random
import time

import anthropic
import openai
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None

# %% Cost estimate (prices change, copy the current ones from the provider's pricing page)
PRICE_PER_MILLION = {"input": 0.15, "output": 0.60}      # example numbers in dollars


def cost(prompt_tokens, completion_tokens):
    return (prompt_tokens * PRICE_PER_MILLION["input"] + completion_tokens * PRICE_PER_MILLION["output"]) / 1_000_000


print(f"one call: ${cost(1_500, 300):.6f}")
print(f"100k calls a month: ${100_000 * cost(1_500, 300):,.2f}")

# %% Cost levers
# 1. Smaller model for easy tasks (classification, extraction), big model for hard ones.
# 2. Shorter prompts: send only the relevant context (this is why RAG exists).
# 3. max_tokens limit.
# 4. Cache answers for repeated questions.
# 5. Batch APIs for non-urgent bulk work.

# %% The errors the SDK raises
ERRORS = {
    openai.AuthenticationError: "wrong or missing key (401), do not retry",
    openai.RateLimitError: "too many requests or no quota (429), wait and retry",
    openai.APITimeoutError: "took too long, retry",
    openai.APIConnectionError: "network problem, retry",
    openai.BadRequestError: "your request is invalid (400), fix it, do not retry",
    openai.InternalServerError: "provider problem (5xx), retry",
}
for error, meaning in ERRORS.items():
    print(f"{error.__name__:24} {meaning}")

# %% Retry with exponential backoff
RETRYABLE = (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError, openai.InternalServerError)


def call_with_retry(func, attempts=5, base_delay=1.0):
    for attempt in range(attempts):
        try:
            return func()
        except RETRYABLE as error:
            if attempt == attempts - 1:
                raise
            delay = base_delay * 2**attempt + random.uniform(0, 0.5)
            print(f"{type(error).__name__}, retry in {delay:.1f}s")
            time.sleep(delay)


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise openai.APIConnectionError(request=None)
    return "success"


print(call_with_retry(flaky, base_delay=0.05))

if client:
    answer = call_with_retry(lambda: client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": "Say hi"}], timeout=20, max_tokens=20))
    print(answer.choices[0].message.content, answer.usage.total_tokens)

# %% Log every call (you will thank yourself later)
def logged(func):
    start = time.perf_counter()
    result = func()
    print(f"latency={time.perf_counter() - start:.3f}s")
    return result


logged(lambda: time.sleep(0.01))

# %% Anthropic SDK looks similar, with small differences
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
if ANTHROPIC_KEY:
    claude = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    message = claude.messages.create(
        model="claude-sonnet-4-5",             # use a current model name
        max_tokens=200,                        # required here
        system="You are concise.",             # system prompt is a separate argument
        messages=[{"role": "user", "content": "What is RAG in one sentence?"}],
    )
    print(message.content[0].text, message.usage.input_tokens, message.usage.output_tokens)
else:
    print("set ANTHROPIC_API_KEY to try Claude")

# %% Differences to remember
# OpenAI:    messages include the system role; answer in choices[0].message.content
# Anthropic: system is its own argument; answer in content[0].text; max_tokens required
# Both:      same ideas for tools, streaming, and structured output
