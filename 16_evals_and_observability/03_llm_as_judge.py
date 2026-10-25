# For open-ended answers, ask another LLM to grade with a clear rubric.
# A fake judge keeps this runnable offline. Swap in a real model for real use.

import json
import os
import re

from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None

# %% A good judge prompt: specific rubric, evidence required, structured output
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

example = JUDGE_PROMPT.format(
    question="How long do I have to return shoes?",
    context="Items can be returned within 30 days of delivery.",
    answer="You can return shoes within 60 days.",
)
print(example)


# %% A fake judge: crude word overlap with the context
def fake_judge(prompt):
    context = re.search(r"Context the assistant was given:\n(.*)\nAssistant answer:", prompt, re.S).group(1)
    answer = re.search(r"Assistant answer: (.*)\n\nScore", prompt, re.S).group(1)
    numbers_in_answer = set(re.findall(r"\d+", answer))
    numbers_in_context = set(re.findall(r"\d+", context))
    faithful = 5 if numbers_in_answer <= numbers_in_context else 1
    return json.dumps({"faithfulness": faithful, "relevance": 4, "clarity": 4, "reason": "numbers checked against context"})


def real_judge(prompt):
    response = client.chat.completions.create(
        model=MODEL, temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


judge = real_judge if client else fake_judge


def grade(question, context, answer):
    raw = judge(JUDGE_PROMPT.format(question=question, context=context, answer=answer))
    return json.loads(raw)


# %% Grade two answers
context = "Items can be returned within 30 days of delivery."
print(grade("How long do I have to return shoes?", context, "You can return shoes within 30 days."))
print(grade("How long do I have to return shoes?", context, "You can return shoes within 60 days."))

# %% Pairwise comparison is often more reliable than absolute scores
PAIR_PROMPT = "Which answer is better for the question? Reply with only A or B.\nQuestion: {q}\nA: {a}\nB: {b}"
print(PAIR_PROMPT.format(q="Refund time?", a="5-7 business days.", b="Soon."))

# %% Known judge weaknesses (and fixes)
BIASES = {
    "position bias":   "prefers the first answer -> run twice with the order swapped",
    "verbosity bias":  "prefers longer answers -> add 'do not reward length' to the rubric",
    "self preference": "prefers its own style -> judge with a different model family",
    "inconsistency":   "scores wobble -> temperature 0, several runs, average",
    "vague rubric":    "write precise criteria with examples of each score",
}
for name, fix in BIASES.items():
    print(f"{name:16} {fix}")

# %% Always check the judge against humans
human = [5, 1, 4, 2, 5, 3]
judge_scores = [5, 1, 4, 3, 5, 2]
agree = sum(abs(h - j) <= 1 for h, j in zip(human, judge_scores)) / len(human)
print("judge within 1 point of humans:", round(agree, 2))
# If agreement is low, fix the rubric before trusting the numbers.
