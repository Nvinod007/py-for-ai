# Observability: when something goes wrong in production you need to see what happened.
# Log every model call with inputs, outputs, latency, tokens, cost, and errors.
# Each line has a short comment saying WHAT it is.

# functools: tools for functions; wraps keeps a decorated function's name.
import functools
# json: dict -> JSON text.
import json
# logging: Python's standard way to record messages.
import logging
# random: random numbers.
import random
# statistics: median and other stats.
import statistics
# time: clocks and sleep().
import time
# uuid: makes unique random ids.
import uuid
# ContextVar: a variable that holds a separate value per request/task.
from contextvars import ContextVar

# basicConfig: set up logging; level=INFO shows info messages; format='%(message)s' prints only the message; force=True overrides old setup.
logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)
# getLogger(name): a named logger used with log.info(...).
log = logging.getLogger("llm")
# trace_id: an id that follows one request; default '-' until set.
trace_id: ContextVar[str] = ContextVar("trace_id", default="-")
# Cost per token in dollars (price per million tokens divided by 1,000,000).
PRICE = {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000}      # dollars per token (example)
# List that collects one record per call.
RECORDS = []


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Structured logs (JSON) are searchable. Plain sentences are not.
# **fields: any extra name=value pairs; builds a dict and logs it as JSON so it can be searched.
def log_event(event, **fields):
    # trace_id.get() reads the id; time.time() = seconds since 1970; {**fields} merges the extras.
    entry = {"event": event, "trace_id": trace_id.get(), "ts": round(time.time(), 3), **fields}
    # log.info(text): write an info-level log line.
    log.info(json.dumps(entry))
    return entry


# Log one example event.
log_event("request_received", user="asha", route="/chat")


# %% A fake model call that reports tokens and sometimes fails
# A pretend model: waits a bit, sometimes fails, reports token counts (tokens = word pieces the model reads and writes).
def fake_model(prompt):
    # sleep(seconds): pauses; random.uniform(a, b): random decimal between a and b.
    time.sleep(random.uniform(0.01, 0.05))
    # random.random(): number 0..1; under 0.15 means ~15% failure.
    if random.random() < 0.15:
        # raise: stops with an error.
        raise TimeoutError("model timed out")
    # f-string: text with values inserted.
    answer = f"echo: {prompt}"
    # len(text) // 4: rough token count (about 4 characters per token).
    return {"text": answer, "prompt_tokens": len(prompt) // 4 + 10, "completion_tokens": len(answer) // 4}


# %% A decorator that traces every call
# A decorator maker: traced('name') returns a decorator that times and logs each call.
def traced(name):
    # The decorator receives the function to wrap.
    def decorator(func):
        # @functools.wraps(func): keeps the original function's name and docs.
        @functools.wraps(func)
        # *args, **kwargs: accept any arguments and pass them on.
        def wrapper(*args, **kwargs):
            # time.perf_counter(): precise stopwatch.
            start = time.perf_counter()
            # The dict describing this call.
            record = {"name": name, "trace_id": trace_id.get(), "status": "ok"}
            # try/except/finally: run the call, note any error, and always record at the end.
            try:
                # Run the real function.
                result = func(*args, **kwargs)
                # dict.update(): add or change several keys at once; cost = tokens x price.
                record.update(
                    prompt_tokens=result["prompt_tokens"],
                    completion_tokens=result["completion_tokens"],
                    cost=result["prompt_tokens"] * PRICE["input"] + result["completion_tokens"] * PRICE["output"],
                )
                return result
            # Catch any error to note it, then raise re-throws it.
            except Exception as error:
                # type(error).__name__: error class name as text.
                record.update(status="error", error=type(error).__name__)
                # Re-throw the same error.
                raise
            # finally: always runs, success or failure.
            finally:
                # Latency = time taken, in milliseconds.
                record["latency_ms"] = round((time.perf_counter() - start) * 1000, 1)
                # append: add the record to the list.
                RECORDS.append(record)
                # Dict comprehension keeps all keys except trace_id; ** unpacks them as arguments.
                log_event("llm_call", **{k: v for k, v in record.items() if k != "trace_id"})
        return wrapper
    return decorator


# @traced('name'): the function below is wrapped by the tracing decorator.
@traced("answer_question")
# Calls the fake model.
def answer_question(question):
    return fake_model(question)


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% One trace id follows a whole user request through every step
# seed(3): makes the random results repeatable.
random.seed(3)
# Run 12 fake requests.
for i in range(12):
    # ContextVar.set(): store a new id; uuid4().hex[:8] = 8 random characters.
    trace_id.set(uuid.uuid4().hex[:8])
    # try/except: ignore failures here since they're already logged.
    try:
        answer_question(f"question number {i}")
    except TimeoutError:
        pass

# %% Dashboards start from these numbers
# List comprehension: only successful calls.
ok = [r for r in RECORDS if r["status"] == "ok"]
# sorted(...): slowest last.
latencies = sorted(r["latency_ms"] for r in RECORDS)
# ':.0%' formats as a percent.
print(f"calls: {len(RECORDS)}, error rate: {1 - len(ok) / len(RECORDS):.0%}")
# statistics.median: middle value (p50); p95 = value 95% of calls are faster than.
print(f"latency p50={statistics.median(latencies):.0f}ms  p95={latencies[int(0.95 * (len(latencies) - 1))]:.0f}ms")
# sum(): total of the values.
print(f"tokens in/out: {sum(r['prompt_tokens'] for r in ok)}/{sum(r['completion_tokens'] for r in ok)}")
# ':.6f' = 6 decimals.
print(f"total cost: ${sum(r['cost'] for r in ok):.6f}")

# %% Averages hide pain. Always look at p95/p99 latency and errors by type.

# %% Tracing multi-step work (RAG, agents): one span per step
# A timing helper used with 'with'.
class Span:
    # __init__: runs when created; self is the object.
    def __init__(self, name):
        self.name = name

    # __enter__: runs when the 'with' block starts.
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    # __exit__: runs when the block ends, even after an error; *exc collects error info.
    def __exit__(self, *exc):
        log_event("span", name=self.name, ms=round((time.perf_counter() - self.start) * 1000, 1))


# Set a fixed id for the demo.
trace_id.set("demo1234")
# 'with' starts and ends the Span automatically; nesting shows steps inside steps.
with Span("rag_request"):
    with Span("retrieve"):
        time.sleep(0.01)
    with Span("generate"):
        time.sleep(0.02)

# %% Tools used for this in real systems
# LangSmith, Langfuse, Arize Phoenix, Helicone, OpenTelemetry + Grafana/Datadog.
# They store traces, let you replay a bad request, and run evals on production samples.

# %% Privacy
# Redact emails, phone numbers, keys before logging. Set retention limits. Restrict who can read logs.
