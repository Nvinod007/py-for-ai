import requests

# Download a web page
response = requests.get("https://api.github.com")
print(response.status_code)  # Should print 200

class Dog:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def bark(self):
    print(f"{self.name} is barking")

  def sit(self):
    print(f"{self.name} is sitting")


dog1=Dog("Buddy", 3)
dog2=Dog("Max", 5)

dog1.bark()
dog2.sit()