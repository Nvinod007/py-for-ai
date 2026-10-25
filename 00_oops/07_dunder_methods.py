# Dunder methods let your objects work with built-in syntax:
# print(), ==, +, len(), and so on.
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class Money:  # class: starts a blueprint
    def __init__(self, dollars):  # __init__: runs when Money is created
        self.dollars = dollars  # save the amount on the object

    def __repr__(self):  # dunder: text for developers, used by repr()
        return f"Money({self.dollars})"  # f-string: puts the value inside the text

    def __str__(self):  # dunder: friendly text, used by print()
        return f"${self.dollars:.2f}"  # :.2f = show 2 decimal places

    def __eq__(self, other):  # dunder: runs when you write a == b
        if not isinstance(other, Money):  # isinstance: True if other is a Money
            return NotImplemented  # special value: "I don't know how to compare this"
        return self.dollars == other.dollars  # == : True if both are equal

    def __add__(self, other):  # dunder: runs when you write a + b
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.dollars + other.dollars)  # builds a new Money with the total


# %%
rent = Money(1200)  # create objects
food = Money(400)

print(rent)             # print: shows text; $1200.00   uses __str__
print(repr(food))       # repr(x): developer text of x; Money(400) uses __repr__
print(rent == Money(1200))  # uses __eq__
print(rent + food)      # uses __add__; $1600.00

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
