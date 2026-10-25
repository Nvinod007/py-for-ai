# instance method  -> needs self (one object)
# class method     -> needs cls  (the class, often used as an alternate constructor)
# static method    -> needs neither (a helper that belongs with the class)


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def birthday(self):
        self.age += 1
        return self.age

    @classmethod
    def from_birth_year(cls, name, birth_year, current_year=2026):
        age = current_year - birth_year
        return cls(name, age)

    @staticmethod
    def is_puppy(age):
        return age < 1


# %%
buddy = Dog("Buddy", 3)
print(buddy.birthday())  # 4

pup = Dog.from_birth_year("Luna", 2026)
print(pup.name, pup.age)          # Luna 0
print(Dog.is_puppy(pup.age))      # Truew
print(Dog.is_puppy(buddy.age))    # False
