# For open-ended answers, ask another LLM to grade with a clear rubric.
# A fake judge keeps this runnable offline. Swap in a real model for real use.
# Each line has a short comment saying WHAT it is.

# json: convert JSON text to/from dicts.
import json
# os: os.environ reads environment variables.
import os
# re: pattern matching in text.
import re

# OpenAI: client class for talking to OpenAI's models.
from openai import OpenAI

# os.environ.get(NAME): reads the key (None if unset).
API_KEY = os.environ.get("OPENAI_API_KEY")
# Model name to use.
MODEL = "gpt-4o-mini"
# Real client only if a key exists, otherwise None.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A good judge prompt: specific rubric, evidence required, structured output
# Prompt template; {question} etc. are blanks filled later; {{ }} prints literal braces.
JUDGE_PROMPT = """You are grading an AI assistant's answer.

Question: {question}
Context the assistant was given:
{context}
Assistant answer: {answer}

Score each criterion from 1 (bad) to 5 (excellent):
- faithfulness: every claim in the answer is supported by the context
- relevance: it answers the question asked
- clarity: it is concise and easy to understand

Return ONLY JSON: {{"faithfulness": int, "relevance": int, "clarity": int, "reason": "one sentence quoting evidence"}}"""

# str.format(name=value): fills the blanks in the template.
example = JUDGE_PROMPT.format(
    question="How long do I have to return shoes?",
    context="Items can be returned within 30 days of delivery.",
    answer="You can return shoes within 60 days.",
)
# Show the finished prompt.
print(example)


# %% A fake judge: crude word overlap with the context
# A pretend judge that needs no internet; it checks if numbers in the answer appear in the context.
def fake_judge(prompt):
    # re.search(pattern, text, re.S).group(1): finds the text between the markers; re.S lets '.' match newlines.
    context = re.search(r"Context the assistant was given:\n(.*)\nAssistant answer:", prompt, re.S).group(1)
    # Same trick for the answer.
    answer = re.search(r"Assistant answer: (.*)\n\nScore", prompt, re.S).group(1)
    # re.findall(r'\d+', text): all digit strings; set(): unique items.
    numbers_in_answer = set(re.findall(r"\d+", answer))
    # Numbers found in the context.
    numbers_in_context = set(re.findall(r"\d+", context))
    # a <= b on sets means 'every item of a is in b'.
    faithful = 5 if numbers_in_answer <= numbers_in_context else 1
    # json.dumps(dict): dict -> JSON text, like a model reply.
    return json.dumps({"faithfulness": faithful, "relevance": 4, "clarity": 4, "reason": "numbers checked against context"})


# The real judge: calls the OpenAI model.
def real_judge(prompt):
    # chat.completions.create(...): ask the model; temperature=0 = least random; response_format json_object = reply must be JSON; messages = chat history.
    response = client.chat.completions.create(
        model=MODEL, temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    # The text of the first reply.
    return response.choices[0].message.content


# Pick the real judge if a key exists, otherwise the fake one.
judge = real_judge if client else fake_judge


# Fills the prompt, asks the judge, parses the JSON reply.
def grade(question, context, answer):
    # Ask the judge.
    raw = judge(JUDGE_PROMPT.format(question=question, context=context, answer=answer))
    # json.loads(text): JSON text -> dict.
    return json.loads(raw)


# %% Grade two answers
# The facts the assistant was given.
context = "Items can be returned within 30 days of delivery."
# One faithful answer and one wrong answer, graded.
print(grade("How long do I have to return shoes?", context, "You can return shoes within 30 days."))
print(grade("How long do I have to return shoes?", context, "You can return shoes within 60 days."))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Pairwise comparison is often more reliable than absolute scores
# A template that asks which of two answers is better.
PAIR_PROMPT = "Which answer is better for the question? Reply with only A or B.\nQuestion: {q}\nA: {a}\nB: {b}"
# format(...) fills the blanks.
print(PAIR_PROMPT.format(q="Refund time?", a="5-7 business days.", b="Soon."))

# %% Known judge weaknesses (and fixes)
# dict: judge weakness -> fix.
BIASES = {
    "position bias":   "prefers the first answer -> run twice with the order swapped",
    "verbosity bias":  "prefers longer answers -> add 'do not reward length' to the rubric",
    "self preference": "prefers its own style -> judge with a different model family",
    "inconsistency":   "scores wobble -> temperature 0, several runs, average",
    "vague rubric":    "write precise criteria with examples of each score",
}
# items(): each key and value; {name:16} pads the text.
for name, fix in BIASES.items():
    print(f"{name:16} {fix}")

# %% Always check the judge against humans
# Scores given by people.
human = [5, 1, 4, 2, 5, 3]
# Scores given by the judge.
judge_scores = [5, 1, 4, 3, 5, 2]
# zip pairs scores; counts pairs within 1 point; abs() = size of difference; divide by total.
agree = sum(abs(h - j) <= 1 for h, j in zip(human, judge_scores)) / len(human)
print("judge within 1 point of humans:", round(agree, 2))
# If agreement is low, fix the rubric before trusting the numbers.
