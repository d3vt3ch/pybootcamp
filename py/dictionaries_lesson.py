student = {
    "name": "Alice",
    "age": 20,
    "grade": "A",
    "courses": ["Math", "Science", "History"]
    
}

# Accessing values
print(student["name"])  # Output: Alice
print(student["age"])   # Output: 20
student["age"] = 21  # Updating age
student["email"] = "alice@email.com" # Adding a new key-value pair

keys = student.keys()  # Get all keys
values = student.values()  # Get all values
items = student.items()  # Get all key-value pairs

print(keys)    # Output: dict_keys(['name', 'age', 'grade', 'courses', 'email'])
print(values)  # Output: dict_values(['Alice', 21, 'A', ['Math', 'Science', 'History'], '
print(items)   # Output: dict_items([('name', 'Alice'), ('age', 21) , ('grade', 'A'), ('courses', ['Math', 'Science', 'History']), ('email', 

for key in student:
    print(f"{key}: {student[key]}")

for key, value in student.items():
    print(f"{key}: {value}")

company = {
    "employees": {
        "Alice": {"age": 30, "position": "Manager"},
        "Bob": {"age": 25, "position": "Developer"}
    },
    "departments": ["HR", "IT", "Sales"]
}

print (company["employees"].items())
print (company["departments"])

student_001 = {
    "name": "John",
    "age": 19,
    "major": "Computer Science",
    "grades": [85, 92, 78]
}

student_002 = {
    "name": "Sarah",
    "age": 20,
    "major": "Biology",
    "grades": [90, 88, 95]
}

student_003 = {
    "name": "Mike",
    "age": 18,
    "major": "Mathematics",
    "grades": [82, 79, 91]
}

student_001["age"] = "20"  # Updating age for student_001

students = [student_001, student_002, student_003]
for student in students:
    print(f"Name: {student['name']}, Age: {student['age']}, Major: {student['major']}, Grades: {student['grades']}")        

for student in students:
    print(f"Student Name: {student['name']}, Major: {student['major']}")