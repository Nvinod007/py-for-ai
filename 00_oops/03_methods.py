# instance method  -> needs self (one object)
# class method     -> needs cls  (the class, often used as an alternate constructor)
# static method    -> needs neither (a helper that belongs with the class)
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class Dog:  # class: starts a blueprint
    def __init__(self, name, age):  # __init__: runs when a Dog is created
        self.name = name  # save name on this dog
        self.age = age  # save age on this dog

    def birthday(self):  # instance method: works on one dog (self)
        self.age += 1  # += : add 1 to the current value
        return self.age  # return: sends a value back to the caller

    @classmethod  # decorator: next method gets the class (cls) instead of an object
    def from_birth_year(cls, name, birth_year, current_year=2026):  # current_year=2026: default value if not given
        age = current_year - birth_year  # work out age with subtraction
        return cls(name, age)  # cls(...): builds a new Dog, same as Dog(name, age)

    @staticmethod  # decorator: plain helper, gets neither self nor cls
    def is_puppy(age):
        return age < 1  # age < 1 gives True or False


# %%
buddy = Dog("Buddy", 3)  # create a Dog
print(buddy.birthday())  # call instance method; 4

pup = Dog.from_birth_year("Luna", 2026)  # call class method on the class itself
print(pup.name, pup.age)          # Luna 0
print(Dog.is_puppy(pup.age))      # call static method; True
print(Dog.is_puppy(buddy.age))    # False

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
