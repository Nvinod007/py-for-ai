# Abstraction: the caller uses speak() and never sees how each animal does it.
# Animal cannot be created on its own. Dog and Cat must implement speak().
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from abc import ABC, abstractmethod  # import: loads tools; ABC = base for abstract classes, abstractmethod = marks a must-implement method


class Animal(ABC):  # Animal(ABC): an abstract class, cannot be created directly
    def __init__(self, name):  # __init__: runs when an object is created
        self.name = name  # save name on the object

    @abstractmethod  # decorator: children MUST write their own version of this method
    def speak(self):
        """Each animal supplies its own sound."""  # triple quotes here = a docstring (description of the method)

    def introduce(self):  # normal method children inherit
        return f"{self.name} says {self.speak()}"  # f-string: puts values inside the text


class Dog(Animal):  # Dog(Animal): child class
    def speak(self):  # fills in the required method
        return "woof"  # return: sends a value back


class Cat(Animal):
    def speak(self):
        return "meow"


# %%
buddy = Dog("Buddy")  # create objects
misty = Cat("Misty")

print(buddy.introduce())  # print: shows text; Buddy says woof
print(misty.introduce())  # Misty says meow

try:  # try: run code that might fail
    Animal("Nobody")  # fails: abstract class cannot be created
except TypeError as error:  # except: catches TypeError; "as error" names it
    print(error)  # Can't instantiate abstract class Animal

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
