# A class is a blueprint. An object is one built copy.
# self is that copy, so each dog keeps its own name.


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} is barking")

    def sit(self):
        print(f"{self.name} is sitting")


# %%
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

dog1.bark()  # Buddy is barking
dog2.sit()   # Max is sitting

print(dog1.name, dog1.age)
print(dog2.name, dog2.age)

# dog1.bark() is the same as Dog.bark(dog1)
# Python passes the object as self for you.
Dog.bark(dog1)
