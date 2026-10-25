# Pydantic: define the shape of data once, get validation, parsing, and JSON for free.
# FastAPI is built on it, and so is structured LLM output.

from datetime import date
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationError


# %% A model
class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None
    active: bool = True


user = User(name="Asha", age=25)
print(user)
print(user.name, user.age, user.active)

# %% It converts types when it safely can
print(User(name="Ben", age="32"))                # "32" -> 32
print(User(name="Chen", age=47, active="yes"))   # "yes" -> True

# %% It rejects bad data with clear errors
try:
    User(name="Dev", age="not a number")
except ValidationError as error:
    print(error)
    print(error.errors()[0]["loc"], error.errors()[0]["type"])

try:
    User(age=5)                                  # name missing
except ValidationError as error:
    print([e["msg"] for e in error.errors()])

# %% Field rules
class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="price in dollars")
    quantity: int = Field(default=1, ge=0, le=1000)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    tags: list[str] = Field(default_factory=list)


print(Product(name="Pen", price=1.5, sku="PEN-0001"))
for bad in [{"name": "P", "price": 1, "sku": "PEN-0001"}, {"name": "Pen", "price": -1, "sku": "bad"}]:
    try:
        Product(**bad)
    except ValidationError as error:
        print(len(error.errors()), "problems:", [e["loc"][0] for e in error.errors()])

# %% Enums and Literal limit choices
class Status(str, Enum):
    TODO = "todo"
    DONE = "done"


class Task(BaseModel):
    title: str
    status: Status = Status.TODO
    priority: Literal["low", "medium", "high"] = "medium"
    due: Optional[date] = None


print(Task(title="Learn pydantic", status="done", due="2026-12-31"))

# %% Nested models
class Address(BaseModel):
    city: str
    zip_code: str


class Customer(BaseModel):
    name: str
    address: Address
    orders: list[int] = []


customer = Customer(name="Asha", address={"city": "Pune", "zip_code": "411001"}, orders=[1, 2])
print(customer.address.city)

# %% Dict and JSON in and out
print(customer.model_dump())
print(customer.model_dump(exclude={"orders"}))
print(customer.model_dump_json(indent=2))
print(Customer.model_validate({"name": "Ben", "address": {"city": "Delhi", "zip_code": "110001"}}))
print(Customer.model_validate_json('{"name": "Chen", "address": {"city": "Goa", "zip_code": "403001"}}'))

# %% Copy and update (models are mutable by default)
updated = user.model_copy(update={"age": 26})
print(user.age, updated.age)

# %% JSON schema (this is what you give an LLM for structured output)
print(list(Product.model_json_schema()["properties"]))
print(Product.model_json_schema()["required"])
