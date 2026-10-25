# Type hints and dataclasses: clean, self-documenting data containers.
# Each line has a short comment saying WHAT it is.

from dataclasses import asdict, dataclass, field, replace  # import: dataclass = auto-builds a class; field = settings per attribute; asdict = object -> dict; replace = copy with changes
from enum import Enum  # Enum: base for a fixed set of named values
from typing import Literal, Optional, TypedDict, Union  # typing: tools for writing type hints

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Type hints
def total_price(prices: list[float], tax: float = 0.1) -> float:  # def: makes a function; "name: type" and "-> type" are hints only; tax=0.1 = default value
    return sum(prices) * (1 + tax)  # sum(x): adds the numbers; return: sends the value back


name: str = "Asha"  # variable with a type hint
scores: dict[str, int] = {"math": 90}  # dict = key: value pairs; hint says str keys, int values
maybe_age: Optional[int] = None          # int or None   (same as int | None); None = "nothing"
id_value: Union[int, str] = "A1"         # same as int | str
mode: Literal["fast", "slow"] = "fast"   # only these exact values
print(total_price([10, 20]))  # print(x): shows x

# %% Hints do not enforce anything at runtime
print(total_price([1]))
print(total_price.__annotations__)  # __annotations__: dict of a function's hints
# Python ignores the hints when running. Use pyright/mypy in your editor to catch
# mistakes, and pydantic (folder 12) to enforce types on incoming data.

# %% dataclass: automatic __init__, __repr__, __eq__
@dataclass  # decorator: auto-writes __init__, printing and == for the class below
class Employee:  # class: a blueprint
    name: str  # field with a type hint (becomes an __init__ argument)
    salary: float
    skills: list[str] = field(default_factory=list)    # default_factory=list: new empty list per object; mutable default done right
    active: bool = True  # field with a default value

    def raise_salary(self, percent: float) -> None:  # method: self = this object; "-> None" = returns nothing
        self.salary *= 1 + percent / 100  # *= : multiply the value in place


e = Employee("Asha", 50000, ["python"])  # create an object
print(e)
e.raise_salary(10)  # call a method
print(e.salary, e == Employee("Asha", 55000.0, ["python"]))  # == : True if all fields match
print(asdict(e))  # asdict(obj): turns the dataclass into a plain dict
print(replace(e, name="Ben"))              # replace(obj, field=value): copy with changes

# %% Enum: a fixed set of named values
class Role(Enum):  # Enum: each name below is one allowed choice
    ADMIN = "admin"
    USER = "user"


print(Role.ADMIN, Role.ADMIN.value, Role("user"), list(Role))  # .value: the stored text; Role("user"): look up by value; list(x): turn items into a list
print(Role.ADMIN == Role("admin"))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% frozen (cannot change) and ordering
@dataclass(frozen=True, order=True)  # frozen=True: fields can't be changed after creation; order=True: allows < and > comparisons
class Point:
    x: int
    y: int


p = Point(1, 2)
print(p, Point(1, 2) < Point(1, 3))  # < compares fields in order
try:  # try: run code that might fail
    p.x = 5  # not allowed on a frozen class
except Exception as error:  # except: catches errors; "as error" names it
    print(type(error).__name__)  # type(x): kind of thing x is; __name__: its name
print({p: "usable as a dict key"})  # {key: value}: dict; frozen objects can be keys

# %% __post_init__: validate or compute after creation
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # init=False: not an __init__ argument, we set it ourselves

    def __post_init__(self):  # special method: runs right after __init__
        if self.width <= 0 or self.height <= 0:  # if/or: runs block when either test is True
            raise ValueError("sizes must be positive")  # raise: throws an error on purpose
        self.area = self.width * self.height


print(Rectangle(3, 4))

# %% TypedDict: hints for plain dicts (common in API code)
class UserRow(TypedDict):  # TypedDict: describes which keys a dict has and their types
    name: str
    age: int


row: UserRow = {"name": "Asha", "age": 25}  # still a normal dict at runtime
print(row)

# %% Dataclass in a list, sorting, grouping
staff = [Employee("A", 3), Employee("B", 1), Employee("C", 2)]  # [..] = list of objects
print([s.name for s in sorted(staff, key=lambda s: s.salary)])  # [x for ...]: list comprehension; sorted(list, key=f): sort by f's result; lambda: tiny one-line function
print(max(staff, key=lambda s: s.salary).name)  # max(list, key=f): biggest by f's result
