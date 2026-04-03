# what list do you want to use?

# list 1 
# fruits = ["apple", "banana", "orange"]

# list 2
# vagetables = ["carrot", "broccoli", "spinach"]

# list 3
# juices = ["orange juice", "apple juice", "grape juice"]

# print (list)
# do you want to add more items to the list? yes or no
# if yes, what item do you want to add?
# do you want to remove any items from the list? yes or no
# if yes, what item do you want to remove?

# the final list is: fruits = ["apple", "banana", "orange"]
print(" ")

print("Welcome to the grocery list manager!")
print("Here are your current lists:")

fruits = ["apple", "banana", "orange"]
vagetables = ("carrot", "broccoli", "spinach")
juices = ["orange juice", "apple juice", "grape juice"]

print("1. Fruits:", fruits)
print("2. Vegetables:", vagetables)
print("3. Juices:", juices) 
print(" ")

print("Which list would you like to manage? (1, 2, or 3)")
list_choice = input("Enter the number of the list you want to manage: ")

if list_choice == "1":
    selected_list = fruits
    list_name = "Fruits"
elif list_choice == "2":
    selected_list = vagetables
    list_name = "Vegetables"
elif list_choice == "3":
    selected_list = juices
    list_name = "Juices"
else:
    print("Invalid choice. Exiting.")
    exit()  

print(f"\nYou have selected the {list_name} list: {selected_list}")
print("\nDo you want to add more items to the list? (yes or no)")
add_choice = input("Enter your choice: ")

if isinstance(selected_list, tuple):
    print(f"\nSorry, the {list_name} list is not modifiable.")
elif add_choice.lower() == "yes":
    new_item = input("What item do you want to add? ")
    selected_list.append(new_item)
    print(f"{new_item} has been added to the {list_name} list.")
else:
    print("No items added to the list.")
print(f"\nThe current {list_name} list is: {selected_list}")

print("\nDo you want to remove any items from the list? (yes or no)")
remove_choice = input("Enter your choice: ")
if remove_choice.lower() == "yes":
    item_to_remove = input("What item do you want to remove? ")
    if isinstance(selected_list, tuple):
        print(f"\nSorry, the {list_name} list is not modifiable.")
    elif item_to_remove in selected_list:
        selected_list.remove(item_to_remove)
        print(f"{item_to_remove} has been removed from the {list_name} list.")
    else:
        print(f"Sorry, the {list_name} list is not modifiable.")


print(f"\nThe final {list_name} list is: {selected_list}")
