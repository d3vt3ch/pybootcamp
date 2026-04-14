
# Inheritance

class Shape: #parent class
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0
    
class Circle(Shape): #child class
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2
    
class Square(Shape): #child class
    def __init__(self, side):
        super().__init__("Square")
        self.side = side

    def area(self):
        return self.side ** 2
    
# Both Circle and Square inherit from Shape, so they can use the area method, but they also have their own implementation of it.

circle = Circle(5)
square = Square(4)

print(circle.name)
print(square.name)

print(circle.area())
print(square.area())

# polymorphism
def print_area(shape): #takes any shape
    print(f"The area of the {shape.name} is: {shape.area()}")

print_area(circle)
print_area(square)

print("\n")
# or with a list
Shape = [Circle(3), Square(5), Circle(2)]

for shape in Shape:
    print_area(shape) # Same code , different results