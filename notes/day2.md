# Day 2

## 📌 INPUT/OUTPUT VALIDATION

```bash

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

```

## 📌 CONDITIONAL STATEMENTS
if-else: 2 conditions
if-elif-else: more than 2 conditions

```bash
weather ="sunny"
temperatture = 75

if weather == "sunny":
    if temperatture > 70:
        print("It's sunny and warm")
    else:
        print("It's sunny but cool")
```


## Create a branch and push the update


✅ STEP 1 — Save your work (IMPORTANT)

Make sure everything is committed first:

git add .
git commit -m "update from day1"
✅ STEP 2 — Switch to main
git checkout main
✅ STEP 3 — Pull latest main (good practice)
git pull origin main
✅ STEP 4 — Merge day1 into main
git merge day1

👉 This brings all your day1 work into main

✅ STEP 5 — Push main to GitHub
git push origin main
✅ STEP 6 — Create new branch day2
git checkout -b day2

👉 Now you're working on fresh branch for today

🔁 Simple flow to remember
day1 → merge → main → push → create day2

