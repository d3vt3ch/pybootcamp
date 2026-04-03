# -- #Write a program that finds the largest and smallest number inlist.

# -- select your list
# -- list 1 : 1 ,3 ,5 ,6
# -- list 2 : 100 ,20 , 1
# -- list 3 : 9,1000, 500, 2000,24

# -- what do you want to do?
# -- select 1 for find the largest number
# -- select 2 for find the smallest number

# -- print the list you have selected
# -- print the largest or smallest number based on your selection    



# Define the lists
list1 = [1, 3, 5, 6]
list2 = [100, 20, 1]
list3 = (9, 1000, 500, 2000, 24)

print("Welcome to the number finder!")
print("Here are your lists:")
print("1. List 1:", list1)
print("2. List 2:", list2)
print("3. List 3:", list3)


selection = int(input("Select your list (1, 2, or 3): "))
if selection == 1:
    selected_list = list1
elif selection == 2:
    selected_list = list2
elif selection == 3:
    selected_list = list3
else:
    print("Invalid selection.")
    exit()
print(f"You have selected: {selected_list}")
action = int(input("What do you want to do? (1 for largest, 2 for smallest): "))
if action == 1:
    result = max(selected_list)
    print(f"The largest number in the list is: {result}")
elif action == 2:
    result = min(selected_list)
    print(f"The smallest number in the list is: {result}")
else:
    print("Invalid action.")

