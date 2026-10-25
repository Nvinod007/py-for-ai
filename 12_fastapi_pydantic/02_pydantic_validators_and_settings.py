# Custom validation, computed values, unions, config, and settings from the environment.

import os
from typing import Annotated, Literal, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)


# %% Validate one field
class Signup(BaseModel):
    username: str
    password: str
    confirm: str

    @field_validator("username")
    @classmethod
    def clean_username(cls, value):
        value = value.strip().lower()
        if not value.isalnum():
            raise ValueError("username must be letters and numbers only")
        return value

    @field_validator("password")
    @classmethod
    def strong_password(cls, value):
        if len(value) < 8:
            raise ValueError("password needs at least 8 characters")
        return value

    # %% Validate several fields together
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm:
            raise ValueError("passwords do not match")
        return self


print(Signup(username="  Asha1 ", password="longenough", confirm="longenough"))
for bad in [
    {"username": "a b", "password": "short", "confirm": "short"},
    {"username": "ok", "password": "longenough", "confirm": "different"},
]:
    try:
        Signup(**bad)
    except ValidationError as error:
        print([e["msg"] for e in error.errors()])


# %% Computed fields
class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height


print(Rectangle(width=3, height=4).model_dump())


# %% Config: strict input, frozen objects, aliases
class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)
    name: str


try:
    Strict(name="x", unexpected=1)
except ValidationError as error:
    print(error.errors()[0]["type"])                       # extra_forbidden
print(Strict(name="  trimmed  "))


class ApiUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_id: int = Field(alias="userId")                   # API uses camelCase, Python uses snake_case


print(ApiUser(userId=5).user_id, ApiUser(user_id=6).user_id)
print(ApiUser(userId=5).model_dump(by_alias=True))


# %% Annotated types are reusable rules
Percent = Annotated[float, Field(ge=0, le=100)]


class Exam(BaseModel):
    score: Percent
    passed: bool


print(Exam(score=88.5, passed=True))


# %% Unions: pick the right shape using a tag
class Cat(BaseModel):
    kind: Literal["cat"]
    lives: int


class Dog(BaseModel):
    kind: Literal["dog"]
    tricks: list[str]


class Owner(BaseModel):
    pet: Union[Cat, Dog] = Field(discriminator="kind")


print(Owner(pet={"kind": "dog", "tricks": ["sit"]}))
print(Owner(pet={"kind": "cat", "lives": 9}))


# %% Settings from environment variables (no secrets in code)
class Settings(BaseModel):
    app_name: str = "demo"
    debug: bool = False
    openai_api_key: str | None = None

    @classmethod
    def from_env(cls):
        return cls(
            app_name=os.environ.get("APP_NAME", "demo"),
            debug=os.environ.get("DEBUG", "false").lower() == "true",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
        )


settings = Settings.from_env()
print(settings.app_name, settings.debug, "key set" if settings.openai_api_key else "no key")
# The pydantic-settings package does this and can read a local .env for you.

# %% Pydantic vs dataclass vs dict
# dict:       no checks
# dataclass:  structure, no validation
# pydantic:   structure + validation + parsing + JSON (use for anything crossing a boundary:
#             API requests, config, LLM output, files)
