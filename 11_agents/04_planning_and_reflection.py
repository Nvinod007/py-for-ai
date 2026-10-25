# Two patterns that make agents more reliable:
#   Plan-and-execute: write a plan first, then do the steps.
#   Reflection: draft -> critique -> improve.
# A scripted fake model keeps this offline. The structure is what matters.

import json

# %% A fake planner and fake worker
def fake_planner(goal):
    return json.dumps({
        "steps": [
            "Collect last month's sales numbers",
            "Find the top 3 products",
            "Write a 2 sentence summary",
        ]
    })


DATA = {
    "Collect last month's sales numbers": {"pen": 120, "book": 340, "lamp": 80, "desk": 210},
}


def fake_worker(step, context):
    if step.startswith("Collect"):
        return DATA[step]
    if step.startswith("Find the top 3"):
        sales = context["Collect last month's sales numbers"]
        return sorted(sales, key=sales.get, reverse=True)[:3]
    if step.startswith("Write"):
        top = context["Find the top 3 products"]
        return f"Top sellers were {', '.join(top)}. Book led the month."
    return "unknown step"


# %% Plan, then execute step by step, keeping results as context
def plan_and_execute(goal):
    plan = json.loads(fake_planner(goal))["steps"]
    print("PLAN:")
    for i, step in enumerate(plan, 1):
        print(f"  {i}. {step}")
    context = {}
    for step in plan:
        context[step] = fake_worker(step, context)
        print(f"DONE: {step} -> {context[step]}")
    return context[plan[-1]]


print(plan_and_execute("Summarize last month's sales"))

# %% Re-plan when a step fails
def execute_with_replan(steps, worker, max_replans=1):
    context, replans = {}, 0
    queue = list(steps)
    while queue:
        step = queue.pop(0)
        try:
            context[step] = worker(step, context)
        except Exception as error:
            if replans >= max_replans:
                raise
            replans += 1
            print(f"step failed ({error}); asking the planner for a new plan")
            queue.insert(0, f"retry: {step}")
            worker = lambda s, c: "recovered"
    return context


print(execute_with_replan(["a", "b"], lambda s, c: 1 / 0 if s == "a" else "ok"))


# %% Reflection: draft -> critique -> revise
def fake_draft(task, feedback=None):
    if feedback is None:
        return "Our product is good."
    return "Our product cuts report time from 3 hours to 10 minutes, with a free 14 day trial."


def fake_critic(draft):
    problems = []
    if len(draft.split()) < 8:
        problems.append("too short")
    if not any(ch.isdigit() for ch in draft):
        problems.append("no concrete numbers")
    return problems


def write_with_reflection(task, max_rounds=3):
    draft, feedback = fake_draft(task), None
    for round_number in range(1, max_rounds + 1):
        problems = fake_critic(draft)
        print(f"round {round_number}: {draft!r} problems={problems}")
        if not problems:
            return draft
        feedback = "; ".join(problems)
        draft = fake_draft(task, feedback)
    return draft


print(write_with_reflection("Write one line of product copy"))

# %% When to use what
# Plan-and-execute: long tasks with clear steps (reports, data pipelines, research).
# ReAct loop (file 01): short tasks where the next step depends on the last result.
# Reflection: when quality matters and you can define "good" (rules, tests, rubric).
# Always cap rounds and steps. More loops mean more cost and more ways to go wrong.
