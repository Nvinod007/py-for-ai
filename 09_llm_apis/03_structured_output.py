# Programs need data, not paragraphs. Make the model return JSON that you validate.
# Each line has a short comment saying WHAT it is.

import json
import os

from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

# os.environ.get(NAME): reads a setting from your terminal; gives None if it is not set.
API_KEY = os.environ.get("OPENAI_API_KEY")
# MODEL = the name of the AI model to use.
MODEL = "gpt-4o-mini"
# OpenAI(api_key=...): creates the object we use to talk to the API; None if there is no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Define the shape you want
# BaseModel (pydantic): a class that describes the data shape and checks it.
class Ticket(BaseModel):
    # Field(description=...): a note about the field; str = text.
    category: str = Field(description="billing, shipping, or technical")
    # Field(ge=1, le=5): ge = at least 1, le = at most 5, otherwise validation fails.
    urgency: int = Field(ge=1, le=5)
    summary: str


# model_json_schema(): the shape written as a JSON schema; .keys() = field names.
print(Ticket.model_json_schema()["properties"].keys())

# %% A stand-in "model" so this runs without a key
# fake_llm: pretends to be the AI; first try gives bad data (urgency 9), second gives good data.
def fake_llm(prompt, attempt=0):
    if attempt == 0:
        return '```json\n{"category": "billing", "urgency": 9, "summary": "double charged"}\n```'
    return '{"category": "billing", "urgency": 4, "summary": "double charged"}'

# %% Never trust raw model text: strip, parse, validate
# parse_ticket(raw): cleans the AI text, turns it into data, and checks it.
def parse_ticket(raw):
    # strip(): remove spaces/newlines at both ends.
    raw = raw.strip()
    # startswith('```'): True if the text begins with the markdown code fence.
    if raw.startswith("```"):
        # strip('`'): remove backticks; removeprefix('json'): cut the word json off the start.
        raw = raw.strip("`").removeprefix("json").strip()
    # json.loads(text): turn JSON text into a dict; model_validate(dict): build a Ticket and raise ValidationError if the data breaks the rules.
    return Ticket.model_validate(json.loads(raw))


print(parse_ticket(fake_llm("x", attempt=1)))

# %% Real structured output (the API enforces your schema)
if client:
    # parse(...): like create() but returns data already shaped like your class; response_format=Ticket = the shape to follow.
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract a support ticket."},
            {"role": "user", "content": "My parcel never arrived and I need it by Friday!"},
        ],
        response_format=Ticket,
    )
    # message.parsed: the answer as a Ticket object.
    print(completion.choices[0].message.parsed)

# %% Rules
# 1. Always validate with pydantic, even when the API promises a schema.
# 2. Keep schemas small and fields clearly described.
# 3. Use enums/Literal for fixed choices.
# 4. Handle refusals and empty answers.

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Repair loop: tell the model what was wrong, try again
# extract_ticket: asks the model, validates, and retries up to max_attempts times if the answer is bad.
def extract_ticket(text, llm=fake_llm, max_attempts=3):
    prompt = f"Extract a ticket as JSON with category, urgency (1-5), summary.\nText: {text}"
    # range(n): counts 0 to n-1.
    for attempt in range(max_attempts):
        raw = llm(prompt, attempt)
        try:
            return parse_ticket(raw)
        # JSONDecodeError = text was not valid JSON; ValidationError = JSON broke the rules.
        except (json.JSONDecodeError, ValidationError) as error:
            # str(error).splitlines()[0]: just the first line of the error message.
            print(f"attempt {attempt + 1} invalid: {str(error).splitlines()[0]}")
            # Add the error to the prompt so the model can fix its answer.
            prompt += f"\nYour last answer was invalid ({error}). Return valid JSON only."
    # raise: stop with an error after all attempts fail.
    raise RuntimeError("model never produced valid output")


print(extract_ticket("I was charged twice for my order!"))

# %% JSON mode (valid JSON, but the shape is up to you)
if client:
    # response_format={'type': 'json_object'}: forces the reply to be valid JSON (shape not checked).
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": "Return a JSON object with keys city and country for Paris."}],
    )
    # json.loads: turn the JSON text into a Python dict.
    print(json.loads(response.choices[0].message.content))
