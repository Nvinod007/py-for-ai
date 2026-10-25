# A class is a blueprint. An object is one built copy.
# self is that copy, so each dog keeps its own name.
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class Dog:  # class: keyword that starts a new blueprint named Dog
    def __init__(self, name, age):  # def: makes a function; __init__ runs automatically when a Dog is created
        self.name = name  # self.name: saves name on this one dog
        self.age = age  # self.age: saves age on this one dog

    def bark(self):  # a function inside a class is called a method; self = the dog calling it
        print(f"{self.name} is barking")  # print: shows text; f"...{x}": f-string puts the value of x inside the text

    def sit(self):  # another method
        print(f"{self.name} is sitting")  # f-string again


# %%
dog1 = Dog("Buddy", 3)  # Dog(...): creates an object (a real dog) and runs __init__ with these values
dog2 = Dog("Max", 5)  # a second, separate dog

dog1.bark()  # object.method(): calls bark on dog1 -> Buddy is barking
dog2.sit()   # Max is sitting

print(dog1.name, dog1.age)  # object.attribute: reads a value saved on the object
print(dog2.name, dog2.age)

# %% the long way to call a method
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# dog1.bark() is the same as Dog.bark(dog1)
# Python passes the object as self for you.
Dog.bark(dog1)  # ClassName.method(object): the long way to call a method
