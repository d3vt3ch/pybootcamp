# weather ="sunny"
# temperatture = 75

# if weather == "sunny":
#     if temperatture > 70:
#         print("It's sunny and warm")
#     else:
#         print("It's sunny but cool")

# else:
#     print("Its not sunny")

# weight = float(input("Enter your weight (kg): "))
# height = float(input("Enter your height (cm): "))           

while True:
    try:
        weight = float(input("Enter your weight (kg): "))
        if weight >0:
            break
        else:
            print("Weight must be more than 0")
    except ValueError:
        print("Please enter valid number!")

while True:
    try:
        height = float(input("Enter your height (cm): "))
        if height >0:
            break
        else:
            print("Height must be more than 0")
    except ValueError:
        print("Please enter valid number!")



# Calculate BMI formula
bmi = weight / ((height/100) ** 2)

# Output result
print(f"Your BMI is: {bmi:.2f}")

if bmi>30.0:
    print("Your BMI is Overweight")
elif bmi<18.5:
    print("Your BMI is Underweight")
elif bmi<=24.9:
    print("Your BMI is Normal")
elif bmi<=29.9:
    print("Your BMI is Overweight")
else:
    print("Try again")
