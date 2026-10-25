# Observability: when something goes wrong in production you need to see what happened.
# Log every model call with inputs, outputs, latency, tokens, cost, and errors.

import functools
import json
import logging
import random
import statistics
import time
import uuid
from contextvars import ContextVar

logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)
log = logging.getLogger("llm")
trace_id: ContextVar[str] = ContextVar("trace_id", default="-")
PRICE = {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000}      # dollars per token (example)
RECORDS = []


# %% Structured logs (JSON) are searchable. Plain sentences are not.
def log_event(event, **fields):
    entry = {"event": event, "trace_id": trace_id.get(), "ts": round(time.time(), 3), **fields}
    log.info(json.dumps(entry))
    return entry


log_event("request_received", user="asha", route="/chat")


# %% A fake model call that reports tokens and sometimes fails
def fake_model(prompt):
    time.sleep(random.uniform(0.01, 0.05))
    if random.random() < 0.15:
        raise TimeoutError("model timed out")
    answer = f"echo: {prompt}"
    return {"text": answer, "prompt_tokens": len(prompt) // 4 + 10, "completion_tokens": len(answer) // 4}


# %% A decorator that traces every call
def traced(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            record = {"name": name, "trace_id": trace_id.get(), "status": "ok"}
            try:
                result = func(*args, **kwargs)
                record.update(
                    prompt_tokens=result["prompt_tokens"],
                    completion_tokens=result["completion_tokens"],
                    cost=result["prompt_tokens"] * PRICE["input"] + result["completion_tokens"] * PRICE["output"],
                )
                return result
            except Exception as error:
                record.update(status="error", error=type(error).__name__)
                raise
            finally:
                record["latency_ms"] = round((time.perf_counter() - start) * 1000, 1)
                RECORDS.append(record)
                log_event("llm_call", **{k: v for k, v in record.items() if k != "trace_id"})
        return wrapper
    return decorator


@traced("answer_question")
def answer_question(question):
    return fake_model(question)


# %% One trace id follows a whole user request through every step
random.seed(3)
for i in range(12):
    trace_id.set(uuid.uuid4().hex[:8])
    try:
        answer_question(f"question number {i}")
    except TimeoutError:
        pass

# %% Dashboards start from these numbers
ok = [r for r in RECORDS if r["status"] == "ok"]
latencies = sorted(r["latency_ms"] for r in RECORDS)
print(f"calls: {len(RECORDS)}, error rate: {1 - len(ok) / len(RECORDS):.0%}")
print(f"latency p50={statistics.median(latencies):.0f}ms  p95={latencies[int(0.95 * (len(latencies) - 1))]:.0f}ms")
print(f"tokens in/out: {sum(r['prompt_tokens'] for r in ok)}/{sum(r['completion_tokens'] for r in ok)}")
print(f"total cost: ${sum(r['cost'] for r in ok):.6f}")

# %% Averages hide pain. Always look at p95/p99 latency and errors by type.

# %% Tracing multi-step work (RAG, agents): one span per step
class Span:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        log_event("span", name=self.name, ms=round((time.perf_counter() - self.start) * 1000, 1))


trace_id.set("demo1234")
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
