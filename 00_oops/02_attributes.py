# Instance attributes live on one object (self.name).
# Class attributes live on the class and are shared.
# Each line has a short comment saying WHAT it is.


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

class Dog:  # class: starts a blueprint
    species = "Canis familiaris"  # class attribute: shared by every Dog

    def __init__(self, name):  # __init__: runs when a Dog is created
        self.name = name           # instance attribute: only this dog
        self.tricks = []           # [] = empty list; new list per dog

    def learn(self, trick):  # method: self = this dog, trick = value passed in
        self.tricks.append(trick)  # list.append(x): adds x to the end of the list


# %%
buddy = Dog("Buddy")  # create an object
max_dog = Dog("Max")

buddy.learn("sit")  # call the method: adds "sit" to Buddy's list only
max_dog.learn("roll")

print(buddy.species, buddy.tricks)    # print: shows values; ['sit']
print(max_dog.species, max_dog.tricks)  # ['roll']

# Changing the class attribute is visible on every dog
# that has not set its own species.
Dog.species = "dog"  # ClassName.attr = value: changes the shared value
print(buddy.species, max_dog.species)

# Assigning on the instance hides the class value for that one object.
buddy.species = "good boy"  # object.attr = value: makes a private copy just for buddy
print(buddy.species)   # good boy
print(max_dog.species)  # dog
print(Dog.species)      # dog

# %% nothing rare
# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
