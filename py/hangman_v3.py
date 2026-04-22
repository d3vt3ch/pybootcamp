# hangman game with CRUD functionality
# update creation of new category and deletion of category.
# add feature for saving list of words in a file.
# add highscore dashboard

import random
import json # New: Import for file handling
import os   # New: To check if file exists

# The filename where data will be stored
DATA_FILE = "hangman_words.json"
# New file for scores
SCORE_FILE = "high_scores.json" 

# Default words to use if the file doesn't exist yet 
default_words = {
    "fruits": ["apple", "banana", "cherry", "date", "fig", "grape"],
    "animals": ["cat", "dog", "elephant", "giraffe", "lion", "tiger"],
    "countries": ["usa", "canada", "brazil", "india", "china", "australia"]
}

def load_data():
    """Loads the words dictionary from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return default_words

def save_data():
    """Saves the current words dictionary to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(words, f, indent=4)

# for the score dashboard
def load_scores():
    """Loads the high scores from the JSON file."""
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    return {} # Return empty dict if no scores exist yet

def save_scores():
    """Saves the current scores to the JSON file."""
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)


# Load the data at the very start 
words = load_data()
scores = load_scores()

# --- STAGES AND PLAY_HANGMAN FUNCTIONS ---
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
    
    print("\n--- Welcome to Hangman! ---")
    player_name = input("Enter your name: ").strip().capitalize()
    if not player_name:
        player_name = "Guest"

    # Set lives 
    lives = 6
    print("\n--- Game Starting! ---")

    # DYNAMIC CATEGORY LOADING
    categories = list(words.keys())
    print("Choose a category:")
    for i, name in enumerate(categories, 1):
        print(f"{i}. {name.capitalize()}")
    
    choice = input("Enter the number of the category: ")

     # VALIDATION
    if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
        print("Invalid selection.")
        return

    selected_category = categories[int(choice) - 1]

    if not words[selected_category]:
        print(f"The {selected_category} category is empty! Add words first.")
        return

    # Choose a random word from the list
    chosen_word = random.choice(words[selected_category])
    placeholder = '_' * len(chosen_word)
    
    #print(chosen_word)
    
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
                print(f"The answer was : {chosen_word}\n")
        if chosen_word == display:
            game_over = True
            print(f"\n~~ You win, {player_name}! ~~")

            # Update Score Logic
            scores[player_name] = scores.get(player_name, 0) + 1
            save_scores()
            print(f"Total wins for {player_name}: {scores[player_name]}")

def view_leaderboard():
    """Displays sorted high scores."""
    print("\n==== LEADERBOARD ====")
    if not scores:
        print("No scores recorded yet. Be the first to win!")
    else:
        # Sort scores from highest to lowest
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print(f"{'Player':<15} | {'Wins':<5}")
        print("-" * 25)
        for name, win_count in sorted_scores:
            print(f"{name:<15} | {win_count:<5}")
    print("=====================")


def manage_words():
    global words
    print("\n--- Word Management ---")
    print("1. Create New Category (Create)")
    print("2. Add Word (Create)")
    print("3. View Words (Read)")
    print("4. Edit Word (Update)")
    print("5. Remove Word (Delete)")
    print("6. Remove Category (Delete)")
    print("7. Back to Main Menu")
    
    choice = input("\nSelect an option: ")

    # OPTION 1: CREATE CATEGORY
    if choice == '1':
        print("\n === Create a New Category (Create) ===")
        for category,word_list in words.items():
            print(f"{category.capitalize()}")

        new_cat = input("\nEnter the name of the new category: ").lower().strip()
        if new_cat in words:
            print("That category already exists.")
        else:
            words[new_cat] = []
            save_data() # SAVE CHANGE
            print(f"Category '{new_cat.capitalize()}' created! Now add words using Option 1.")

    # OPTION 2: ADD WORD
    elif choice == '2':

        print("\n === Add Word (Create) ===")
        categories = list(words.keys())
        
        print("\nSelect category to add word to:")
        for i, name in enumerate(categories, 1):
            print(f"{i}. {name.capitalize()}")

        cat_choice = input("Enter number: ")
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            selected_cat = categories[int(cat_choice) - 1]
            new_word = input(f"Enter word for {selected_cat}: ").strip().lower()
            if new_word in words[selected_cat]:
                print("Word already exists.")
            else:
                words[selected_cat].append(new_word)
                save_data() # SAVE CHANGE
                print(f"'{new_word}' added to {selected_cat}!")
        else:
            print("Invalid category.")

    # OPTION 3: VIEW WORDS
    elif choice == '3':
        print("\n=== View Words (Read) ===")

        # Display all categories and their words
        for category, word_list in words.items():
            print(f"{category.capitalize()}: {', '.join(word_list)}")

    elif choice == '4':
        print("\n=== Edit Word (Update) ===")
        categories = list(words.keys())
        for i, name in enumerate(categories, 1):
            print(f"{i}. {name.capitalize()}")

        cat_choice = input("Select the category number to edit a word in: ")
        
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            selected_cat = categories[int(cat_choice) - 1]
            print(f"\nCurrent words in {selected_cat}: {', '.join(words[selected_cat])}")
            
            old_word = input("Enter the word you want to edit: ").strip().lower()
            if old_word in words[selected_cat]:
                new_word = input("Enter the new word: ").strip().lower()
                index = words[selected_cat].index(old_word)
                words[selected_cat][index] = new_word
                save_data() # SAVE CHANGE
                print(f"'{old_word}' updated to '{new_word}' in {selected_cat}.")
            else:
                print(f"'{old_word}' not found in {selected_cat}.")
        else:
            print("Invalid category selection.")

    # OPTION 5: REMOVE WORD (UPDATED DYNAMIC LOGIC)
    elif choice == '5':
        print("\n=== Remove Word (Delete) ===")
        categories = list(words.keys())
        for i, name in enumerate(categories, 1): 
            print(f"{i}. {name.capitalize()}")

        cat_choice = input("Select the category number to remove a word from: ")
        
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            selected_cat = categories[int(cat_choice) - 1]
            print(f"Current words in {selected_cat}: {', '.join(words[selected_cat])}")
            
            word_to_remove = input("Enter the word you want to remove: ").strip().lower()
            if word_to_remove in words[selected_cat]:
                words[selected_cat].remove(word_to_remove)
                save_data() # SAVE CHANGE
                print(f"'{word_to_remove}' removed from {selected_cat}.")
            else:
                print(f"'{word_to_remove}' not found in {selected_cat}.")
        else:
            print("Invalid category selection.")

    # OPTION 6: REMOVE Category (UPDATED DYNAMIC LOGIC)
    elif choice == '6':
        print("\n=== Remove Category (Delete) ===")
        categories = list(words.keys())
        for i, name in enumerate(categories, 1): 
            print(f"{i}. {name.capitalize()}")

        cat_choice = input("Select the category number to remove: ")
        
        # Validation to prevent crashes 
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            # Bridging the gap
            selected_cat = categories[int(cat_choice) - 1]
            # Using 'del' to remove the key-value pair from the dictionary
            del words[selected_cat]
            save_data() # SAVE CHANGE
            print(f"Success: The category '{selected_cat}' and all its words have been removed.")
        
        else:
            print("Invalid selection. No category was removed.")
            

    # Exiting using option 7

    elif choice == '7':
        print("Returning to main menu.")
        return
    else:
        print("Invalid choice")

# --- THE MAIN CONTROLLER ---
while True:
    print("\n==== HANGMAN SYSTEM ====")
    print("1. Play Hangman")
    print("2. View Leaderboard") # New Option
    print("3. Manage Words")
    print("4. Exit")
    
    main_choice = input("What would you like to do? ")
    
    if main_choice == '1':
        play_hangman()
    elif main_choice == '2':
        view_leaderboard()
    elif main_choice == '3':
        manage_words()
    elif main_choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")
