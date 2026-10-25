# Two patterns that make agents more reliable:
#   Plan-and-execute: write a plan first, then do the steps.
#   Reflection: draft -> critique -> improve.
# A scripted fake model keeps this offline. The structure is what matters.
# Each line has a short comment saying WHAT it is.

# json: convert dicts to/from JSON text.
import json

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A fake planner and fake worker
# Pretend planner: returns a fixed list of steps as JSON text (a real LLM would write it).
def fake_planner(goal):
    return json.dumps({
        "steps": [
            "Collect last month's sales numbers",
            "Find the top 3 products",
            "Write a 2 sentence summary",
        ]
    })


# Fake data the worker can 'collect'.
DATA = {
    "Collect last month's sales numbers": {"pen": 120, "book": 340, "lamp": 80, "desk": 210},
}


# Pretend worker: does one step; 'context' holds results from earlier steps. str.startswith(x) checks the beginning of the text.
def fake_worker(step, context):
    if step.startswith("Collect"):
        return DATA[step]
    if step.startswith("Find the top 3"):
        sales = context["Collect last month's sales numbers"]
        # sorted(dict, key=sales.get, reverse=True): keys ordered by their value, biggest first; [:3] keeps three.
        return sorted(sales, key=sales.get, reverse=True)[:3]
    if step.startswith("Write"):
        top = context["Find the top 3 products"]
        # ', '.join(list): joins items into one text with commas.
        return f"Top sellers were {', '.join(top)}. Book led the month."
    return "unknown step"


# %% Plan, then execute step by step, keeping results as context
# Makes a plan first, then runs each step in order.
def plan_and_execute(goal):
    # json.loads: JSON text -> dict; ['steps'] picks the list.
    plan = json.loads(fake_planner(goal))["steps"]
    print("PLAN:")
    # enumerate(list, 1): gives (number, item) pairs starting from 1.
    for i, step in enumerate(plan, 1):
        print(f"  {i}. {step}")
    context = {}
    for step in plan:
        context[step] = fake_worker(step, context)
        print(f"DONE: {step} -> {context[step]}")
    return context[plan[-1]]


print(plan_and_execute("Summarize last month's sales"))

# %% Re-plan when a step fails
# Runs steps; if one fails, retries it once (max_replans) with a new worker.
def execute_with_replan(steps, worker, max_replans=1):
    context, replans = {}, 0
    # list(steps): makes a copy so the original isn't changed.
    queue = list(steps)
    while queue:
        # pop(0): removes and returns the first item.
        step = queue.pop(0)
        try:
            context[step] = worker(step, context)
        # except: catches an error so the program doesn't crash; 'as error' holds the error.
        except Exception as error:
            if replans >= max_replans:
                # raise (alone): re-throws the same error.
                raise
            replans += 1
            print(f"step failed ({error}); asking the planner for a new plan")
            # insert(0, x): puts x at the front of the list.
            queue.insert(0, f"retry: {step}")
            # lambda: a tiny one-line function; this replacement always returns 'recovered'.
            worker = lambda s, c: "recovered"
    return context


# 1 / 0 deliberately crashes (division by zero) for step 'a' to trigger a replan.
print(execute_with_replan(["a", "b"], lambda s, c: 1 / 0 if s == "a" else "ok"))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Reflection: draft -> critique -> revise
# Pretend writer: first draft is weak; with feedback it returns a better one.
def fake_draft(task, feedback=None):
    if feedback is None:
        return "Our product is good."
    return "Our product cuts report time from 3 hours to 10 minutes, with a free 14 day trial."


# Pretend reviewer: returns a list of problems found in the draft.
def fake_critic(draft):
    problems = []
    if len(draft.split()) < 8:
        problems.append("too short")
    # any(...): True if at least one item is True; ch.isdigit() checks for a number character.
    if not any(ch.isdigit() for ch in draft):
        problems.append("no concrete numbers")
    return problems


# Loop: draft -> critique -> rewrite, up to max_rounds times.
def write_with_reflection(task, max_rounds=3):
    draft, feedback = fake_draft(task), None
    for round_number in range(1, max_rounds + 1):
        problems = fake_critic(draft)
        # !r in an f-string shows the value with quotes (repr).
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
