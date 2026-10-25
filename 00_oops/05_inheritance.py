# A child class reuses the parent and adds or replaces behavior.
# super() calls the parent version so you do not copy it.


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        return f"{self.name} says woof"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow"


# %%
dog = Dog("Buddy", "lab")
cat = Cat("Misty")

print(dog.speak(), dog.breed)
print(cat.speak())
print(isinstance(dog, Animal))  # True: a Dog is an Animal
print(isinstance(cat, Dog))     # False
