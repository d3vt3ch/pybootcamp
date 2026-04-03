fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True]
empty_list = []

# Accessing elements
print(fruits[0])  # Output: apple
print(numbers[2])  # Output: 3
print(mixed[1])  # Output: 42
print(empty_list)  # Output: []
print("")

print(fruits[0])  # Output: apple
print(fruits[-1])  # Output: orange
print(numbers[1:4])  # Output: [2, 3, 4] , start from 1 till before 4
print(numbers[:3])  # Output: [1,2,3], start from 0 till before 3
print(numbers[2:])  # Output: [3,4,5],print from 2 till the end
print(mixed[0:3])  # Output: [42, 3.14], start from 1 till before 3
print("")

fruits.append("grape")  # Add "grape" to the end of the list
print(fruits)  # Output: ['apple', 'banana', 'orange', 'grape']
fruits.insert(1, "kiwi")  # Insert "kiwi" at index 1
print(fruits)  # Output: ['apple', 'kiwi', 'banana', 'orange', 'grape']
fruits.remove("banana")  # Remove "banana" from the list
print(fruits)  # Output: ['apple', 'kiwi', 'orange', 'grape']
# fruits.pop()  # Remove the last element ("grape")
# print(fruits)  # Output: ['apple', 'kiwi', 'orange']
# fruits.pop(1)  # Remove the element at index 1 ("kiwi")
# print(fruits)  # Output: ['apple', 'orange']

print("")
popped = fruits.pop()   # Remove and return the last element ("orange")
print(fruits) 

fruits.sort()  # Sort the list in place
print(fruits)  # Output: ['apple', 'kiwi']  

fruits.reverse()  # Reverse the list in place
print(fruits)  # Output: ['kiwi', 'apple']     

len(fruits)  # Get the number of elements in the list
print(len(fruits))  # Output: 2 

"apple" in fruits  # Check if "apple" is in the list
print("apple" in fruits)  # Output: True
"banana" in fruits  # Check if "banana" is in the list
print("banana" in fruits)  # Output: False

fruits + ["mango"]
fruits * 2  # Repeat the list twice
print(fruits + ["mango"])  # Output: ['kiwi', 'apple', 'mango']
print(fruits * 2)  # Output: ['kiwi', 'apple', 'kiwi', 'apple']
print(len(fruits))  # Output: 2


fruits.clear()  # Remove all elements from the list
print(fruits)  # Output: []    
print(len(fruits)) # Output: 0