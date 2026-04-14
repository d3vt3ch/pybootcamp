
# functions with parameters
def greet_person(name):
    print(f"hello, {name}!")

greet_person("Amir")


#function with return values

def add_numbers(a,b):
    return a+b

result = add_numbers(5,3)
print(result) # 8

#default parameteres

def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}!"

print(greet_with_title("Amir"))
print(greet_with_title("Amir","Dr."))

# *args - variable number of arguments

def sum_all(*args):
    return sum(args)

print(sum_all(1,2,3,4,5)) 

# **kwargs - keyword arguments

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Amir", age=25 , city="Kuala lumpur")

# combine *args and **kwargs

def flexible_functions(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

flexible_functions(1,2,3, name="Ammar", age=11)

# Lambda functions (anonymous functions)

square = lambda x: x**2
print(square(5))

add = lambda x,y: x+y
print(add(3,4))

numbers=[1,2,3,4,5,6,7,8,9,10]

for n in numbers:
    if n%2!=0:
        print(f"{n} = is prime number")
    else:
        print(f"{n}")