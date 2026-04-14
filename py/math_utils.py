def add(a, b):
    """Returns the sum of a and b."""
    return a + b

def multiply(a, b):
    """Returns the product of a and b."""
    return a * b

def factorial(n):    
    """Returns the factorial of n."""
    if n<=1:
        return 1
    return n * factorial(n-1)

PI = 3.14159

class Calculator:
    """A simple calculator class."""
    def __init__(self):
        self.history = []

    def calculate(self, operation, a, b):
        """Performs the given operation on a and b."""
        if operation == 'add':
            result = add(a, b)
        elif operation == 'multiply':
            result = multiply(a, b)
        else:
            result = None   

        self.history.append(f"{operation}({a}, {b}) = {result}")
        return result