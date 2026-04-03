# Exercise:
# 1.Create a system that stores student grades as tuples (name, subject, grade)
# and uses sets to find unique subjects and students. grades = [  ("Alice", "Math", 85),  ("Bob", "Science", 92),  ("Alice", "Science", 78),  ("Charlie", "Math", 90),  ("Bob", "Math", 88),  ("Alice", "English", 95) ]


grades = [
    ("Alice", "Math", 85),
    ("Bob", "Science", 92),
    ("Alice", "Science", 78),
    ("Charlie", "Math", 90),
    ("Bob", "Math", 88),
    ("Alice", "English", 95)
]   




#method 1
print("\n--- Using for loops to assign value from the matrix table to variable ---\n")
students = set() # to store unique student names
subjects = set() # to store unique subjects  

for name, subject, grade in grades:   # unpacking the tuple into name, subject, grade
    students.add(name)                # add the name to the students set
    subjects.add(subject)             # add the subject to the subjects set
    
print("Unique students:", students) # print("Unique subjects:", subjects)
print("Unique subjects:", subjects) # print("Unique students:", students) #

#method 2
print("\n--- Using Set Comprehension ---\n")
students = {student for student, subject, grade in grades}  # set comprehension to create a set of unique student names
print("Unique Students:", students)                         # set comprehension to create a set of unique subjects
subjects = {subject for student, subject, grade in grades}
print("Unique Subjects:", subjects)

#method 3
print("\n--- Using Unique location ---\n")
students = set()                    # to store unique student names
subjects = set()                    # to store unique subjects     
for grade in grades:
    students.add(grade[0])          # add the name (first element of the tuple) to the students set
    subjects.add(grade[1])          # add the subject (second element of the tuple) to the subjects set 
print("Unique students:", students) # print("Unique subjects:", subjects)
print("Unique subjects:", subjects) # print("Unique students:", students) #