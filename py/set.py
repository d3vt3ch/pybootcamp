set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1)  # Output: {1, 2, 3, 4}
print(set2)  # Output: {3, 4, 5, 6}

print("\nunion:")
print(set1.union(set2))  # Output: {1, 2, 3, 4, 5, 6}
print("\nintersection:")
print(set1.intersection(set2))  # Output: {3, 4}
print("\ndifference:")
print(set1.difference(set2))  # Output: {1, 2}
print("\nsymmetric difference:")
print(set1.symmetric_difference(set2))  # Output: {1, 2, 5, 6}
