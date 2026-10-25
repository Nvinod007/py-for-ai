# 06 Production monitoring checklist for AI systems

## Before launch

- [ ] Eval set with at least 30-50 real cases, including edge, refusal, and safety cases.
- [ ] Release gate: a pass rate below the threshold blocks the deploy.
- [ ] Load test with realistic traffic and long inputs.
- [ ] Spending limits and alerts in the provider dashboard.
- [ ] Timeouts, retries with backoff, and a fallback (smaller model, cached answer, friendly message).
- [ ] Input limits (max length, rate limit per user).
- [ ] Output checks (schema, banned content, no secrets).
- [ ] Prompt injection reviewed: untrusted text cannot trigger risky tools.
- [ ] Human approval on irreversible actions.

## What to log on every request

| Field | Why |
|---|---|
| trace id | follow one request across services |
| user or tenant id (not raw personal data) | find who is affected |
| model name and prompt version | explain behavior changes |
| input and output (redacted) | debug bad answers |
| retrieved chunk ids | debug RAG failures |
| tool calls and results | debug agents |
| tokens in/out and cost | control spend |
| latency and each step's time | find slow parts |
| errors with type | spot provider problems |
| user feedback (thumbs up/down) | cheapest quality signal |

## Dashboards and alerts

| Metric | Alert when |
|---|---|
| error rate | above 2% for 5 minutes |
| p95 latency | above your target |
| cost per day | above budget or jumps 2x |
| refusal rate | sudden rise or fall |
| thumbs-down rate | rises after a release |
| retrieval hit rate or empty results | falls |
| token usage per request | grows (prompt bloat) |

## After launch, keep improving

1. Sample real conversations weekly and read them.
2. Add every real failure to the eval set.
3. Re-run evals on every change: prompt, model, retrieval settings, tools.
4. Roll out changes gradually (a small percentage of users first) and compare.
5. Pin model versions. Providers update models and behavior can shift.
6. Review costs monthly: can a smaller model handle the easy requests?

## Incident routine

1. Stop the harm (feature flag, disable a tool, switch to a safer model).
2. Find the trace and reproduce the problem.
3. Fix, add an eval case, and re-run the full set.
4. Write down what happened and what changed.

## Practice

1. Take any folder 09-12 example and add the `traced` decorator from `04_tracing_logging_and_cost.py`.
2. Add 10 new cases to `05_eval_harness_compare_prompts.py`, including 2 prompt injections.
3. Write a one-page runbook for "the model started giving wrong answers".
