# Abstraction: the caller uses speak() and never sees how each animal does it.
# Animal cannot be created on its own. Dog and Cat must implement speak().

from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def speak(self):
        """Each animal supplies its own sound."""

    def introduce(self):
        return f"{self.name} says {self.speak()}"


class Dog(Animal):
    def speak(self):
        return "woof"


class Cat(Animal):
    def speak(self):
        return "meow"


# %%
buddy = Dog("Buddy")
misty = Cat("Misty")

print(buddy.introduce())  # Buddy says woof
print(misty.introduce())  # Misty says meow

try:
    Animal("Nobody")
except TypeError as error:
    print(error)  # Can't instantiate abstract class Animal
