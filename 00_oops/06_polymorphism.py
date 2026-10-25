# Polymorphism: one call site, many types.
# The loop does not care which animal it has. It only needs speak().


class Dog:
    def speak(self):
        return "woof"


class Cat:
    def speak(self):
        return "meow"


class Duck:
    def speak(self):
        return "quack"


def chorus(animals):
    for animal in animals:
        print(animal.speak())


# %%
chorus([Dog(), Cat(), Duck()])
# woof
# meow
# quack

# Python does not require a shared parent class.
# If the object has speak(), the call works. That is duck typing.
