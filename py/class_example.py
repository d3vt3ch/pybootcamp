
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
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount}")
            return f"Deposited ${amount}. New balance: ${self.balance}."
        else:
            return "Deposit amount must be positive."
        
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: ${amount}")
            return f"Withdrew ${amount}. New balance: ${self.balance}."
        else:
            return "Withdrawal amount must be positive and less than or equal to the balance."
        
    def get_balance(self):
        return f"Current balance: ${self.balance}."

    def get_transaction_history(self):
        return self.transaction_history
    
# using the BankAccount class
account = BankAccount("12345", "Amir", 1000)

print(account.get_balance())
print(account.deposit(500))
print(account.withdraw(200))
print(account.get_transaction_history())
print(account.get_balance())

# using the BankAccount class
account = BankAccount("22345", "Amira", 10000)

print(account.get_balance())
print(account.deposit(500))
print(account.withdraw(200))
print(account.get_transaction_history())
print(account.get_balance())