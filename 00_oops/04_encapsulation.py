# Keep data behind methods so callers cannot set nonsense values.
# A single leading underscore means "internal, please don't touch".
# A property looks like an attribute but runs code on get/set.
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class BankAccount:  # class: starts a blueprint
    def __init__(self, owner, balance):  # __init__: runs when an account is created
        self.owner = owner  # public attribute: anyone may use it
        self._balance = 0  # _name: internal by convention, don't touch from outside
        self.deposit(balance)  # call our own method so the checks run

    @property  # decorator: lets you write account.balance without ()
    def balance(self):
        return self._balance  # return: sends the value back

    def deposit(self, amount):  # method: adds money
        if amount <= 0:  # if: runs the next lines only when the test is True
            raise ValueError("amount must be positive")  # raise: stops with an error; ValueError = bad value
        self._balance += amount  # += : add to the current value

    def withdraw(self, amount):  # method: takes money out
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("not enough money")
        self._balance -= amount  # -= : subtract from the current value


# %%
account = BankAccount("Ada", 100)  # create an object
print(account.balance)  # print: shows text; 100, read through the property

account.deposit(50)  # call a method
account.withdraw(30)
print(account.balance)  # 120

try:  # try: run code that might fail
    account.withdraw(1000)  # this will raise an error
except ValueError as error:  # except: catches that error type; "as error" names it
    print(error)  # not enough money

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
