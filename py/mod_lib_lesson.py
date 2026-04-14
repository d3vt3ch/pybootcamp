
# Import functions from the math module
import sys

from math_utils import add, multiply, factorial, PI, Calculator

result = add(5, 3)
print(f"Addition result: {result}")

result = multiply(5, 3)
print(f"\nMultiplication result: {result}\n")


import os
import sys
import datetime
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Add current directory to sys.path

now = datetime.datetime.now()
today = datetime.date.today()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

print(f"Now date: {now}") # Print the current date and time
print(f"Today's date: {today}") #  Print today's date
print(f"Formatted date: {formatted_date}") # Print the formatted date and time

random_number = random.randint(1, 100)
random_choice = random.choice(['apple', 'banana', 'cherry'])
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)

print(f"Random number : {random_number}") # Print a random number between 1 and 100
print(f"Random choice: {random_choice}") # Print a random choice from the list
print(f"Shuffled numbers: {numbers}") # Print the shuffled list of numbers  
