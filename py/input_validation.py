
name=input("Enter your name: ")
height = float(input("Enter your height (cm): ")) #convert to float


#input validation

while True:
    try:
        age = int(input("Enter your age: "))
        if age > 0:
            break
        else:
            print("Age must be postive!")
    except ValueError:
        print("Please enter a valid number!")


# Output validation
print(f"Hello, {name}!")
print(f"You are {age} years old and {height} cm")

if age >=18:
    print("You are an adult")
else:
    print("You are a minor")