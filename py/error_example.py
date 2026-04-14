
# Basic exception handling

try:
    number = int(input("Enter a number : "))
    result = 10 / number
    print(f"Result: {result}")
except ValueError:
    print("Invalid input! Please enter a number.")
except ZeroDivisionError:
    print("Cannot divide by Zero!")

#Using else and finally

try:
    file = open("data.txt", "r")
except FileNotFoundError:
    print("file not found!")
else:
    #executes if no exception occured
    content = file.read()
    print("File read successfully")
    print(content)
finally:
    # Always executes
    if 'file' in locals() and not file.closed:
        file.close()
        print("Cleanup completed")

# Raising exceptions
def validate_age(age): 
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

try:
    validate_age(151)
except ValueError as e:
    print(f"Validation Error: {e}")