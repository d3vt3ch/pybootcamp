# hangman game with CRUD functionality
import random
global lives
# Create a list of words
words = {
    "fruits": ["apple", "banana", "cherry", "date", "fig", "grape"],
    "animals": ["cat", "dog", "elephant", "giraffe", "lion", "tiger"],
    "countries": ["usa", "canada", "brazil", "india", "china", "australia"]
}

stages = [  # final state: head, torso, both arms, and both legs
    """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |     / \\
    -
    """,
    # head, torso, both arms, and one leg
    """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |     / 
    -
    """,
    # head, torso, and both arms
    """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |      
    -
    """,
    # head, torso, and one arm
    """
    --------
    |      |
    |      O
    |     \\|
    |      |
    |     
    -
    """,
    # head and torso
    """
    --------
    |      |
    |      O
    |      |
    |      |
    |     
    -
    """,
    # head only
    """
    --------
    |      |
    |      O
    |    
    |      
    |     
    -
    """,
    # initial empty state
    """
    --------
    |      |
    |      
    |    
    |      
    |     
    -
    """
]

def play_hangman():
    # Set lives 
    lives = 6
    print("\n--- Game Starting! ---")

    # Choose a category
    category = input("Choose a category \n" \
    "1.fruits \n" \
    "2.animals \n" \
    "3.countries \n"
    "Enter the number of the category you want to play:  ")

    # Choose a random word from the list
    if category == '1':
        if not words["fruits"]:
            print("The fruits category is empty. Please add words to the category before playing.")
            return
        chosen_word = random.choice(words["fruits"])
        #check if the category is empty
        
    elif category == '2':
        chosen_word = random.choice(words["animals"])
        if not words["animals"]:
            print("The animals category is empty. Please add words to the category before playing.")
            return
    elif category == '3':
        chosen_word = random.choice(words["countries"])
        if not words["countries"]:
            print("The countries category is empty. Please add words to the category before playing.")
            return

    #print(chosen_word)

    placeholder = '_'*len(chosen_word)
    print(placeholder)

    game_over = False
    correct_letters = []


    while not game_over:
        # Ask user to guess a letter and make it lowercase
        guess = input("Guess a letter: ").lower()    
        
        display = ''

        for letter in chosen_word:
            if letter == guess:
                display += guess
                correct_letters.append(guess)
            
            elif letter in correct_letters:
                display += letter   

            else:
                display += '_' 

        if guess not in chosen_word:
            lives -= 1
            print(f"Your have {lives} lives left.")
            

        print(stages[lives])
        print(display)
        if lives == 0:
                game_over = True
                print("\n You lose! \n ")
                print(f"The answer is : {chosen_word}\n")

        if chosen_word == display:
            game_over = True
            print("\n~~ You win! ~~")
            print(f"The word is : {display}\n")


def manage_words():
    global words
    print("\n--- Word Management ---")
    print("1. Add Word (Create)")
    print("2. View Words (Read)")
    print("3. Edit Word (Update)")
    print("4. Remove Word (Delete)")
    print("5. Back to Main Menu")
    
    choice = input("\nSelect an option: ")

    if choice == '1':
        print("\n === Add Word (Create) ===")
        category = input("Enter category \n" \
        "1. fruits \n" \
        "2. animals \n" \
        "3. countries\n"
        "\nEnter the number of the category you want to add a word to:  ")
        
        if category not in ['1', '2', '3']:
            print("Category does not exist. Please select a valid category.")
            manage_words()

        category_map = {'1': 'fruits', '2': 'animals', '3': 'countries'}
        # error if category doesn't exist
        category = category_map.get(category, None) # Map the input to the category name

        print(f"Adding a new word to {category} category.\n")
        print(f"{category.capitalize()}: {', '.join(words[category])}")
        new_word = input("\nEnter the new word: ").strip()

        #check if the word already exists in the category
        if category and new_word in words[category]:
            print(f"{new_word} already exists in {category}.")  
            manage_words()
        elif category in words:
            words[category].append(new_word)
            print(f"{new_word} added to {category}.")
        else:
            print("Invalid category.")
            manage_words()

    elif choice == '2':
        print("\n=== View Words (Read) ===")
        # Display all categories and their words
        for category, word_list in words.items():
            print(f"{category.capitalize()}: {', '.join(word_list)}")
            
        # do you want to update the word list? (yes/no)
        update_choice = input("\nDo you want to update the word list? (y/n): ")
        if update_choice == 'y':
            manage_words()  # Call the manage_words function to allow updating
        elif update_choice == 'n':
            print("Returning to main menu.")
            manage_words()  # Return to the main menu
        else:
            print("Invalid choice, returning to main menu.")
            manage_words()

    elif choice == '3':
        print("\n=== Edit Word (Update) ===")
        category = input("Enter category \n" \
        "1. fruits \n" \
        "2. animals \n" \
        "3. countries\n"
        "\nEnter the number of the category you want to edit a word in:  ")
        
        if category not in ['1', '2', '3']:
            print("Category does not exist. Please select a valid category.")
            manage_words()

        category_map = {'1': 'fruits', '2': 'animals', '3': 'countries'}
        category = category_map.get(category, None) # Map the input to the category name

        if category in words:
            print(f"\nCurrent words in {category}: {', '.join(words[category])}")
            old_word = input("\nEnter the word you want to edit: ")
            if old_word in words[category]:
                new_word = input("Enter the new word: ")
                index = words[category].index(old_word)
                words[category][index] = new_word
                print(f"{old_word} has been updated to {new_word} in {category}.")
            else:
                print(f"{old_word} not found in {category}.")
        else:
            print("Invalid category.")

    elif choice == '4':
        print("\n=== Remove Word (Delete) ===")
        category = input("Enter category \n" \
        "1. fruits \n" \
        "2. animals \n" \
        "3. countries\n"
        "\nEnter the number of the category you want to remove a word from:  ")

        if category not in ['1', '2', '3']:
            print("Category does not exist. Please select a valid category.")
            manage_words()

        category_map = {'1': 'fruits', '2': 'animals', '3': 'countries'}
        category = category_map.get(category, None) # Map the input to the category name
       

        if category in words:
            print(f"Current words in {category}: {', '.join(words[category])}")
            word_to_remove = input("\nEnter the word you want to remove: ")
            if word_to_remove in words[category]:
                words[category].remove(word_to_remove)
                print(f"{word_to_remove} has been removed from {category}.")
            else:
                print(f"{word_to_remove} not found in {category}.")
        else:
            print("Invalid category.")
    elif choice == '5':
        print("Returning to main menu.")
    else:
        print("Invalid choice, returning to main menu.")

# --- THE MAIN CONTROLLER ---
while True:
    print("\n==== HANGMAN SYSTEM ====")
    print("1. Play Hangman")
    print("2. Manage Words")
    print("3. Exit")
    
    main_choice = input("What would you like to do? ")
    
    if main_choice == '1':
        play_hangman()
    elif main_choice == '2':
        manage_words()
    elif main_choice == '3':
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")
