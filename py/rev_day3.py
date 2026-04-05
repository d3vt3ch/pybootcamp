
grades = [
    ("Alice", "Math", 85),
    ("Bob", "Science", 92),
    ("Alice", "Science", 78),
    ("Charlie", "Math", 90),
    ("Bob", "Math", 88),
    ("Alice", "English", 95),
]

print(grades)

# Find unique students

students = set()
for name, subject,grade in grades:
    students.add(name)

print (students)

subjects = set()
for name, subject, grade in grades:
    subjects.add(subject)

print (subjects)


students={student for student, subject, grade in grades}
print(students)

subjects={subject for student, subject,grade in grades}
print (subjects)

for grade in grades:
    students.add(grade[0])
    subjects.add(grade[1])

print(students)
print(subjects)