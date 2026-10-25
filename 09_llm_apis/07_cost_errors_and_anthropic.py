# Cost math, handling API errors, and the Anthropic (Claude) SDK.
# Each line has a short comment saying WHAT it is.

import os
import random
import time

import anthropic
import openai
from openai import OpenAI

# os.environ.get(NAME): reads a setting from your terminal; gives None if it is not set.
API_KEY = os.environ.get("OPENAI_API_KEY")
# MODEL = the name of the AI model to use.
MODEL = "gpt-4o-mini"
# OpenAI(api_key=...): creates the object that talks to the API; None if there is no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Cost estimate (prices change, copy the current ones from the provider's pricing page)
# Dictionary of prices in dollars per 1 million tokens (input = what you send, output = what AI writes).
PRICE_PER_MILLION = {"input": 0.15, "output": 0.60}      # example numbers in dollars


# cost: tokens x price, divided by 1,000,000 (1_000_000 = underscores just make big numbers readable).
def cost(prompt_tokens, completion_tokens):
    return (prompt_tokens * PRICE_PER_MILLION["input"] + completion_tokens * PRICE_PER_MILLION["output"]) / 1_000_000


# f"{x:.6f}": show 6 decimals; :, adds thousand commas.
print(f"one call: ${cost(1_500, 300):.6f}")
print(f"100k calls a month: ${100_000 * cost(1_500, 300):,.2f}")

# %% The errors the SDK raises
# ERRORS: maps each error type the SDK can raise to what it means.
ERRORS = {
    openai.AuthenticationError: "wrong or missing key (401), do not retry",
    openai.RateLimitError: "too many requests or no quota (429), wait and retry",
    openai.APITimeoutError: "took too long, retry",
    openai.APIConnectionError: "network problem, retry",
    openai.BadRequestError: "your request is invalid (400), fix it, do not retry",
    openai.InternalServerError: "provider problem (5xx), retry",
}
# items(): gives key and value together; __name__ = the error's name; :24 pads to 24 characters.
for error, meaning in ERRORS.items():
    print(f"{error.__name__:24} {meaning}")

# %% Retry with exponential backoff
# A tuple of errors worth retrying (temporary problems).
RETRYABLE = (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError, openai.InternalServerError)


# call_with_retry: tries func again after temporary errors, waiting longer each time (exponential backoff).
def call_with_retry(func, attempts=5, base_delay=1.0):
    for attempt in range(attempts):
        # try/except: run the code and catch the listed errors instead of crashing.
        try:
            return func()
        except RETRYABLE as error:
            # On the last attempt, `raise` re-throws the error.
            if attempt == attempts - 1:
                raise
            # 2**attempt: doubles each time (1, 2, 4...); random.uniform(0, 0.5): a random extra wait so many callers don't retry together.
            delay = base_delay * 2**attempt + random.uniform(0, 0.5)
            # type(error).__name__: the error's name.
            print(f"{type(error).__name__}, retry in {delay:.1f}s")
            # sleep: wait that many seconds.
            time.sleep(delay)


# A counter in a dictionary so flaky() can change it.
calls = {"n": 0}


# flaky: fails twice on purpose, then succeeds, to test the retry.
def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise openai.APIConnectionError(request=None)
    return "success"


# base_delay=0.05: tiny wait so the demo is fast.
print(call_with_retry(flaky, base_delay=0.05))

if client:
    # lambda: a tiny unnamed function; here it wraps the API call so it can be retried. timeout=20: give up after 20s; max_tokens=20: limit the answer length.
    answer = call_with_retry(lambda: client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": "Say hi"}], timeout=20, max_tokens=20))
    # usage.total_tokens: tokens used in total.
    print(answer.choices[0].message.content, answer.usage.total_tokens)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Cost levers
# 1. Smaller model for easy tasks (classification, extraction), big model for hard ones.
# 2. Shorter prompts: send only the relevant context (this is why RAG exists).
# 3. max_tokens limit.
# 4. Cache answers for repeated questions.
# 5. Batch APIs for non-urgent bulk work.

# %% Log every call (you will thank yourself later)
# logged: runs func and prints how long it took (latency).
def logged(func):
    start = time.perf_counter()
    result = func()
    print(f"latency={time.perf_counter() - start:.3f}s")
    return result


# lambda wraps time.sleep(0.01) so logged can call it.
logged(lambda: time.sleep(0.01))

# %% Anthropic SDK looks similar, with small differences
# Reads the Claude key from the terminal settings (None if not set).
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
if ANTHROPIC_KEY:
    # anthropic.Anthropic(api_key=...): creates the Claude client.
    claude = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    # claude.messages.create(...): sends a message to Claude and returns its reply.
    message = claude.messages.create(
        # model: which Claude model to use.
        model="claude-sonnet-4-5",             # use a current model name
        max_tokens=200,                        # required here
        system="You are concise.",             # system prompt is a separate argument
        messages=[{"role": "user", "content": "What is RAG in one sentence?"}],
    )
    # content[0].text: Claude's answer; usage.input_tokens/output_tokens: tokens in and out.
    print(message.content[0].text, message.usage.input_tokens, message.usage.output_tokens)
else:
    print("set ANTHROPIC_API_KEY to try Claude")

# %% Differences to remember
# OpenAI:    messages include the system role; answer in choices[0].message.content
# Anthropic: system is its own argument; answer in content[0].text; max_tokens required
# Both:      same ideas for tools, streaming, and structured output
