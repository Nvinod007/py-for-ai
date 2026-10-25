# Keep data behind methods so callers cannot set nonsense values.
# A single leading underscore means "internal, please don't touch".
# A property looks like an attribute but runs code on get/set.


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = 0
        self.deposit(balance)

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("not enough money")
        self._balance -= amount


# %%
account = BankAccount("Ada", 100)
print(account.balance)  # 100, read through the property

account.deposit(50)
account.withdraw(30)
print(account.balance)  # 120

try:
    account.withdraw(1000)
except ValueError as error:
    print(error)  # not enough money

# %%
