# Polymorphism: one call site, many types.
# The loop does not care which animal it has. It only needs speak().
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class Dog:  # class: starts a blueprint
    def speak(self):  # method: self = the object calling it
        return "woof"  # return: sends a value back


class Cat:
    def speak(self):
        return "meow"


class Duck:
    def speak(self):
        return "quack"


def chorus(animals):  # def: makes a function; animals = a list passed in
    for animal in animals:  # for: repeats once for each item in the list
        print(animal.speak())  # print: shows text; calls speak on whatever object this is


# %%
chorus([Dog(), Cat(), Duck()])  # [..] = a list; Dog() creates an object
# woof
# meow
# quack

# Python does not require a shared parent class.
# If the object has speak(), the call works. That is duck typing.

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
