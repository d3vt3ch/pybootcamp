
# Basic class definition

class Person:
    # Class attribute (shared by all instances)
    species = "Homo sapiens"

    # Constructor Method
    def __init__(self, name, age):
        #instance attributes
        self.name = name
        self.age = age

    #instance method
    def introduce(self):
        return f"Hi , I'm {self.name} and I'm {self.age} years old."
    
    # method with parameters
    def have_birthday(self):
        self.age +=1
        return f"Happy birthday! {self.name} is now {self.age}."
    
# Creating objects (instances)
person1 = Person("Amir", 29)
person2 = Person("Ammar", 11)

print(person1.name)
print(person1.age)

# Calling methods
print(person1.introduce())
print(person1.have_birthday())

# Class attributes
print(Person.species)
print(person1.species)

class BankAccount:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0: