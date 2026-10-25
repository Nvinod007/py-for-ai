# Pydantic: define the shape of data once, get validation, parsing, and JSON for free.
# FastAPI is built on it, and so is structured LLM output.
# Each line has a short comment saying WHAT it is.

# date: a calendar date type (year, month, day).
from datetime import date
# Enum: a fixed set of allowed named values.
from enum import Enum
# Literal: only these exact values allowed; Optional[X]: X or None.
from typing import Literal, Optional

# BaseModel: base class for data shapes; Field: extra rules for a field; ValidationError: the error raised for bad data.
from pydantic import BaseModel, Field, ValidationError


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A model
# class X(BaseModel): defines a data shape; each 'name: type' line is a field; '= value' is its default.
class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None
    active: bool = True


# Creating the model checks and converts the data automatically.
user = User(name="Asha", age=25)
print(user)
print(user.name, user.age, user.active)

# %% It converts types when it safely can
# Pydantic converts the text to the right type when it safely can.
print(User(name="Ben", age="32"))                # "32" -> 32
print(User(name="Chen", age=47, active="yes"))   # "yes" -> True

# %% It rejects bad data with clear errors
# try/except: run code and catch the error instead of crashing.
try:
    User(name="Dev", age="not a number")
# error.errors() = list of problems; 'loc' = which field, 'type' = kind of error, 'msg' = message.
except ValidationError as error:
    print(error)
    print(error.errors()[0]["loc"], error.errors()[0]["type"])

try:
    User(age=5)                                  # name missing
except ValidationError as error:
    print([e["msg"] for e in error.errors()])

# %% Field rules
# Field(...) rules: min_length/max_length = text size, gt = greater than, ge = greater or equal, le = less or equal, pattern = regex the text must match, default_factory=list = new empty list each time.
class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="price in dollars")
    quantity: int = Field(default=1, ge=0, le=1000)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    tags: list[str] = Field(default_factory=list)


print(Product(name="Pen", price=1.5, sku="PEN-0001"))
# Product(**bad): ** turns a dict into named arguments.
for bad in [{"name": "P", "price": 1, "sku": "PEN-0001"}, {"name": "Pen", "price": -1, "sku": "bad"}]:
    try:
        Product(**bad)
    except ValidationError as error:
        print(len(error.errors()), "problems:", [e["loc"][0] for e in error.errors()])

# %% Enums and Literal limit choices
# Enum: only 'todo' or 'done' are allowed.
class Status(str, Enum):
    TODO = "todo"
    DONE = "done"


# Literal[...]: value must be exactly one of these; Optional[date]: a date or None (text '2026-12-31' is parsed).
class Task(BaseModel):
    title: str
    status: Status = Status.TODO
    priority: Literal["low", "medium", "high"] = "medium"
    due: Optional[date] = None


print(Task(title="Learn pydantic", status="done", due="2026-12-31"))

# %% Nested models
# A model used inside another model.
class Address(BaseModel):
    city: str
    zip_code: str


# Nested model: 'address' must fit the Address shape; a dict is converted automatically.
class Customer(BaseModel):
    name: str
    address: Address
    orders: list[int] = []


# Pass a nested dict; pydantic builds the Address object.
customer = Customer(name="Asha", address={"city": "Pune", "zip_code": "411001"}, orders=[1, 2])
print(customer.address.city)

# %% Dict and JSON in and out
# model_dump(): model -> plain dict; exclude={...} leaves fields out.
print(customer.model_dump())
print(customer.model_dump(exclude={"orders"}))
# model_dump_json(indent=2): model -> pretty JSON text.
print(customer.model_dump_json(indent=2))
# model_validate(dict): dict -> model with checks.
print(Customer.model_validate({"name": "Ben", "address": {"city": "Delhi", "zip_code": "110001"}}))
# model_validate_json(text): JSON text -> model with checks.
print(Customer.model_validate_json('{"name": "Chen", "address": {"city": "Goa", "zip_code": "403001"}}'))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Copy and update (models are mutable by default)
# model_copy(update={...}): a copy with some fields changed.
updated = user.model_copy(update={"age": 26})
print(user.age, updated.age)

# %% JSON schema (this is what you give an LLM for structured output)
# model_json_schema(): the model described as JSON schema; ['properties'] lists fields, ['required'] lists must-have fields.
print(list(Product.model_json_schema()["properties"]))
print(Product.model_json_schema()["required"])
