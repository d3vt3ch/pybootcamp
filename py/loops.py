

for i in range(5): #from 0 till before 5
    print(i)

print("")

for i in range (1,6): #from 1 till before 6
    print(i)

print("")
for i in range(0,10,2): #from 0 till before 10, with step 2
    print (i)

print("")

count = 0
while count <5:   #from 0 till before 5, keep running 
    print (count)
    count +=1      #add 1 everytime

print("")

#nested loops


for i in range(2): #run, exit it when i hit before 2
    for j in range(3): #run, exit it when j hit before 3
        print(f"({i},{j})")   #once done plus +1


# existing examples
for i in range(5):  # from 0 till before 5
    print(i)

print("")

for i in range(1, 6):  # from 1 till before 6
    print(i)

print("")

for i in range(0, 10, 2):  # from 0 till before 10, with step 2
    print(i)

print("")

count = 0
while count < 5:  # from 0 till before 5, keep running
    print(count)
    count += 1  # add 1 every time

print("")

# nested loops
for i in range(2):  # run, exit it when i hits before 2
    for j in range(3):  # run, exit it when j hits before 3
        print(f"({i},{j})")  # once done plus +1

print("\n--- Multiplication Table ---\n")


def multiplication_table(size=10, start=1, end=None):
    """
    Print a multiplication table.
    - size: width of table (largest column multiplier)
    - start: first row and column number
    - end: last row number (defaults to size)
    """
    if end is None:
        end = size

    # Header
    print("   ", end="")
    for j in range(start, size + 1):
        print(f"{j:4}", end="")
    print()
    print("-" * ((size - start + 2) * 4))

    # Table body
    for i in range(start, end + 1):
        print(f"{i:2} |", end="")
        for j in range(start, size + 1):
            print(f"{i * j:4}", end="")
        print()


if __name__ == "__main__":
    n = int(input("Table size (e.g. 10): "))
    multiplication_table(size=n, start=1, end=n)