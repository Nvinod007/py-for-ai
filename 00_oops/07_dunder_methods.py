# Dunder methods let your objects work with built-in syntax:
# print(), ==, +, len(), and so on.


class Money:
    def __init__(self, dollars):
        self.dollars = dollars

    def __repr__(self):
        return f"Money({self.dollars})"

    def __str__(self):
        return f"${self.dollars:.2f}"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.dollars == other.dollars

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.dollars + other.dollars)


# %%
rent = Money(1200)
food = Money(400)

print(rent)             # $1200.00   uses __str__
print(repr(food))       # Money(400) uses __repr__
print(rent == Money(1200))
print(rent + food)      # $1600.00

# %%
