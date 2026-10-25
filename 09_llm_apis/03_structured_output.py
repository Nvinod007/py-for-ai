# Programs need data, not paragraphs. Make the model return JSON that you validate.

import json
import os

from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None


# %% Define the shape you want
class Ticket(BaseModel):
    category: str = Field(description="billing, shipping, or technical")
    urgency: int = Field(ge=1, le=5)
    summary: str


print(Ticket.model_json_schema()["properties"].keys())

# %% A stand-in "model" so this runs without a key
def fake_llm(prompt, attempt=0):
    if attempt == 0:
        return '```json\n{"category": "billing", "urgency": 9, "summary": "double charged"}\n```'
    return '{"category": "billing", "urgency": 4, "summary": "double charged"}'


# %% Never trust raw model text: strip, parse, validate
def parse_ticket(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").removeprefix("json").strip()
    return Ticket.model_validate(json.loads(raw))


print(parse_ticket(fake_llm("x", attempt=1)))

# %% Repair loop: tell the model what was wrong, try again
def extract_ticket(text, llm=fake_llm, max_attempts=3):
    prompt = f"Extract a ticket as JSON with category, urgency (1-5), summary.\nText: {text}"
    for attempt in range(max_attempts):
        raw = llm(prompt, attempt)
        try:
            return parse_ticket(raw)
        except (json.JSONDecodeError, ValidationError) as error:
            print(f"attempt {attempt + 1} invalid: {str(error).splitlines()[0]}")
            prompt += f"\nYour last answer was invalid ({error}). Return valid JSON only."
    raise RuntimeError("model never produced valid output")


print(extract_ticket("I was charged twice for my order!"))

# %% Real structured output (the API enforces your schema)
if client:
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract a support ticket."},
            {"role": "user", "content": "My parcel never arrived and I need it by Friday!"},
        ],
        response_format=Ticket,
    )
    print(completion.choices[0].message.parsed)

# %% JSON mode (valid JSON, but the shape is up to you)
if client:
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": "Return a JSON object with keys city and country for Paris."}],
    )
    print(json.loads(response.choices[0].message.content))

# %% Rules
# 1. Always validate with pydantic, even when the API promises a schema.
# 2. Keep schemas small and fields clearly described.
# 3. Use enums/Literal for fixed choices.
# 4. Handle refusals and empty answers.
