# Instance attributes live on one object (self.name).
# Class attributes live on the class and are shared.


class Dog:
    species = "Canis familiaris"  # shared by every Dog

    def __init__(self, name):
        self.name = name           # only this dog
        self.tricks = []           # new list per dog

    def learn(self, trick):
        self.tricks.append(trick)


# %%
buddy = Dog("Buddy")
max_dog = Dog("Max")

buddy.learn("sit")
max_dog.learn("roll")

print(buddy.species, buddy.tricks)    # ['sit']
print(max_dog.species, max_dog.tricks)  # ['roll']

# Changing the class attribute is visible on every dog
# that has not set its own species.
Dog.species = "dog"
print(buddy.species, max_dog.species)

# Assigning on the instance hides the class value for that one object.
buddy.species = "good boy"
print(buddy.species)   # good boy
print(max_dog.species)  # dog
print(Dog.species)      # dog
