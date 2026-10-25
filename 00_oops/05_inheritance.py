# A child class reuses the parent and adds or replaces behavior.
# super() calls the parent version so you do not copy it.
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class Animal:  # parent class (base class)
    def __init__(self, name):  # __init__: runs when an object is created
        self.name = name  # save name on the object

    def speak(self):  # method every animal gets
        return f"{self.name} makes a sound"  # f-string: puts the value of self.name inside the text


class Dog(Animal):  # Dog(Animal): Dog is a child of Animal and gets all its methods
    def __init__(self, name, breed):
        super().__init__(name)  # super(): the parent class; runs the parent's __init__
        self.breed = breed  # extra attribute only Dogs have

    def speak(self):  # same name as parent: replaces (overrides) it
        return f"{self.name} says woof"


class Cat(Animal):  # Cat also inherits from Animal
    def speak(self):  # overrides the parent speak
        return f"{self.name} says meow"


# %%
dog = Dog("Buddy", "lab")  # create objects
cat = Cat("Misty")  # Cat has no __init__, so it uses Animal's

print(dog.speak(), dog.breed)  # print: shows values
print(cat.speak())
print(isinstance(dog, Animal))  # isinstance(obj, Class): True if obj is that class or a child of it
print(isinstance(cat, Dog))     # False

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
