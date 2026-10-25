# Custom validation, computed values, unions, config, and settings from the environment.
# Each line has a short comment saying WHAT it is.

# os: talk to the operating system; here os.environ reads environment variables.
import os
# Annotated: attach extra rules to a type; Literal: exact allowed values; Union: one of several types.
from typing import Annotated, Literal, Union

# BaseModel: data shape; ConfigDict: model settings; Field: field rules; ValidationError: bad data error; computed_field: a field calculated from others; field_validator/model_validator: your own check functions.
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Validate one field
# A model with custom checks.
class Signup(BaseModel):
    username: str
    password: str
    confirm: str

    # @field_validator('x'): runs the method below on field x to check or clean it.
    @field_validator("username")
    # @classmethod: method that gets the class (cls) instead of an object.
    @classmethod
    # value.strip().lower() removes outer spaces and lowercases; isalnum() = only letters/digits; raise ValueError = reject the data.
    def clean_username(cls, value):
        value = value.strip().lower()
        if not value.isalnum():
            raise ValueError("username must be letters and numbers only")
        return value

    @field_validator("password")
    @classmethod
    # len(value): number of characters.
    def strong_password(cls, value):
        if len(value) < 8:
            raise ValueError("password needs at least 8 characters")
        return value

    # %% Validate several fields together
    # @model_validator(mode='after'): runs after all fields are set, to compare fields together.
    @model_validator(mode="after")
    # self = the finished model object; return it if OK.
    def passwords_match(self):
        if self.password != self.confirm:
            raise ValueError("passwords do not match")
        return self


# Valid example: the username is cleaned to 'asha1'.
print(Signup(username="  Asha1 ", password="longenough", confirm="longenough"))
# Two invalid examples; each prints its error messages.
for bad in [
    {"username": "a b", "password": "short", "confirm": "short"},
    {"username": "ok", "password": "longenough", "confirm": "different"},
]:
    try:
        Signup(**bad)
    except ValidationError as error:
        print([e["msg"] for e in error.errors()])


# %% Computed fields
# A model with a calculated field.
class Rectangle(BaseModel):
    width: float
    height: float

    # @computed_field + @property: 'area' looks like a field and is calculated when read.
    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height


print(Rectangle(width=3, height=4).model_dump())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Config: strict input, frozen objects, aliases
# ConfigDict(extra='forbid') rejects unknown fields; frozen=True makes it read-only; str_strip_whitespace=True trims text.
class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)
    name: str


try:
    Strict(name="x", unexpected=1)
except ValidationError as error:
    print(error.errors()[0]["type"])                       # extra_forbidden
print(Strict(name="  trimmed  "))


# populate_by_name=True lets you use either the alias or the real name.
class ApiUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # Field(alias='userId'): accept/produce the name 'userId' for this field.
    user_id: int = Field(alias="userId")                   # API uses camelCase, Python uses snake_case


print(ApiUser(userId=5).user_id, ApiUser(user_id=6).user_id)
# model_dump(by_alias=True): output uses the alias names.
print(ApiUser(userId=5).model_dump(by_alias=True))


# %% Annotated types are reusable rules
# Annotated[float, Field(...)]: a reusable type 'float between 0 and 100'.
Percent = Annotated[float, Field(ge=0, le=100)]


# Uses the reusable Percent type.
class Exam(BaseModel):
    score: Percent
    passed: bool


print(Exam(score=88.5, passed=True))


# %% Unions: pick the right shape using a tag
# Literal['cat']: this field can only ever be 'cat'; it works as a tag.
class Cat(BaseModel):
    kind: Literal["cat"]
    lives: int


class Dog(BaseModel):
    kind: Literal["dog"]
    tricks: list[str]


# Union[Cat, Dog]: either shape; discriminator='kind' says look at 'kind' to choose.
class Owner(BaseModel):
    pet: Union[Cat, Dog] = Field(discriminator="kind")


print(Owner(pet={"kind": "dog", "tricks": ["sit"]}))
print(Owner(pet={"kind": "cat", "lives": 9}))


# %% Settings from environment variables (no secrets in code)
# Settings: configuration values with defaults.
class Settings(BaseModel):
    app_name: str = "demo"
    debug: bool = False
    openai_api_key: str | None = None

    @classmethod
    # Builds Settings from environment variables; os.environ.get(NAME, default) returns the default if unset.
    def from_env(cls):
        return cls(
            app_name=os.environ.get("APP_NAME", "demo"),
            debug=os.environ.get("DEBUG", "false").lower() == "true",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
        )


# Create settings from the environment.
settings = Settings.from_env()
print(settings.app_name, settings.debug, "key set" if settings.openai_api_key else "no key")
# The pydantic-settings package does this and can read a local .env for you.

# %% Pydantic vs dataclass vs dict
# dict:       no checks
# dataclass:  structure, no validation
# pydantic:   structure + validation + parsing + JSON (use for anything crossing a boundary:
#             API requests, config, LLM output, files)
