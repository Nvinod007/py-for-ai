# Type hints and dataclasses: clean, self-documenting data containers.

from dataclasses import asdict, dataclass, field, replace
from enum import Enum
from typing import Literal, Optional, TypedDict, Union

# %% Type hints
def total_price(prices: list[float], tax: float = 0.1) -> float:
    return sum(prices) * (1 + tax)


name: str = "Asha"
scores: dict[str, int] = {"math": 90}
maybe_age: Optional[int] = None          # int or None   (same as int | None)
id_value: Union[int, str] = "A1"         # same as int | str
mode: Literal["fast", "slow"] = "fast"   # only these exact values
print(total_price([10, 20]))

# %% Hints do not enforce anything at runtime
print(total_price([1]))
print(total_price.__annotations__)
# Python ignores the hints when running. Use pyright/mypy in your editor to catch
# mistakes, and pydantic (folder 12) to enforce types on incoming data.

# %% dataclass: automatic __init__, __repr__, __eq__
@dataclass
class Employee:
    name: str
    salary: float
    skills: list[str] = field(default_factory=list)    # mutable default done right
    active: bool = True

    def raise_salary(self, percent: float) -> None:
        self.salary *= 1 + percent / 100


e = Employee("Asha", 50000, ["python"])
print(e)
e.raise_salary(10)
print(e.salary, e == Employee("Asha", 55000.0, ["python"]))
print(asdict(e))
print(replace(e, name="Ben"))              # copy with changes

# %% frozen (cannot change) and ordering
@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int


p = Point(1, 2)
print(p, Point(1, 2) < Point(1, 3))
try:
    p.x = 5
except Exception as error:
    print(type(error).__name__)
print({p: "usable as a dict key"})

# %% __post_init__: validate or compute after creation
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("sizes must be positive")
        self.area = self.width * self.height


print(Rectangle(3, 4))

# %% Enum: a fixed set of named values
class Role(Enum):
    ADMIN = "admin"
    USER = "user"


print(Role.ADMIN, Role.ADMIN.value, Role("user"), list(Role))
print(Role.ADMIN == Role("admin"))

# %% TypedDict: hints for plain dicts (common in API code)
class UserRow(TypedDict):
    name: str
    age: int


row: UserRow = {"name": "Asha", "age": 25}
print(row)

# %% Dataclass in a list, sorting, grouping
staff = [Employee("A", 3), Employee("B", 1), Employee("C", 2)]
print([s.name for s in sorted(staff, key=lambda s: s.salary)])
print(max(staff, key=lambda s: s.salary).name)
