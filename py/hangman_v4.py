# hangman game with CRUD functionality
# using sqlite for managing the data.

import random
import sqlite3

# --- DATABASE CONFIGURATION ---
DB_NAME = "hangman.db"

def init_db():
    """Initializes the database and populates default words if empty."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enable foreign key support for cascading deletes
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            word TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            player_name TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0
        )
    """)

    # Populate with default words if database is brand new
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_words = {
            "fruits": ["apple", "banana", "cherry", "date", "fig", "grape"],
            "animals": ["cat", "dog", "elephant", "giraffe", "lion", "tiger"],
            "countries": ["usa", "canada", "brazil", "india", "china", "australia"]
        }
        for cat, word_list in default_words.items():
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
            cat_id = cursor.lastrowid
            for w in word_list:
                cursor.execute("INSERT INTO words (category_id, word) VALUES (?, ?)", (cat_id, w))
    
    conn.commit()
    conn.close()

# Initialize DB at startup
init_db()

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

# --- CORE FUNCTIONS ---

def play_hangman():
    
    print("\n--- Welcome to Hangman! ---")
    player_name = input("Enter your name: ").strip().capitalize()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get categories from DB
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall() # Returns a list of tuples [(id, name), ...]

    print("\nChoose a category:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat[1].capitalize()}")

    choice = input("Enter the number: ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
        print("Invalid selection.")
        conn.close()
        return

    selected_cat_id = categories[int(choice) - 1][0]
    selected_cat_name = categories[int(choice) - 1][1]

    # Get random word from DB for selected category
    cursor.execute("SELECT word FROM words WHERE category_id = ? ORDER BY RANDOM() LIMIT 1", (selected_cat_id,))
    result = cursor.fetchone()

    if not result:
        print(f"The {selected_cat_name} category is empty! Add words first.")
        conn.close()
        return

    chosen_word = result[0].lower()
    conn.close() # Close early as we have our word

    lives = 6
    placeholder = '_' * len(chosen_word)
    correct_letters = []
    game_over = False

    print(f"\nCategory: {selected_cat_name.capitalize()}")
    print(placeholder)

    while not game_over:
        guess = input("Guess a letter: ").lower()    
        display = ''

        for letter in chosen_word:
            if letter == guess or letter in correct_letters:
                display += letter
                if letter == guess and guess not in correct_letters:
                    correct_letters.append(guess)
            else:
                display += '_' 

        if guess not in chosen_word:
            lives -= 1
            print(f"Wrong! {lives} lives left.")

        print(stages[lives])
        print(display)
        if lives == 0:
                game_over = True
                print("\n You lose! \n ")
                print(f"The answer was : {chosen_word}\n")
        if chosen_word == display:
            game_over = True
            print(f"\n~~ You win, {player_name}! ~~")

            # UPDATE SCORE IN SQLITE
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scores (player_name, wins) VALUES (?, 1)
                ON CONFLICT(player_name) DO UPDATE SET wins = wins + 1
            """, (player_name,))
            conn.commit()
            
            cursor.execute("SELECT wins FROM scores WHERE player_name = ?", (player_name,))
            print(f"Total wins for {player_name}: {cursor.fetchone()[0]}")
            conn.close()

def view_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, wins FROM scores ORDER BY wins DESC")
    rows = cursor.fetchall()
    conn.close()

    print("\n==== LEADERBOARD ====")
    if not rows:
        print("No scores recorded yet.")
    else:
        print(f"{'Player':<15} | {'Wins':<5}")
        print("-" * 25)
        for name, wins in rows:
            print(f"{name:<15} | {wins:<5}")
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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")


    # OPTION 1: CREATE CATEGORY
    if choice == '1':
        print("\n === Create a New Category (Create) ===")
        new_cat = input("New category name: ").lower().strip()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (new_cat,))
            conn.commit()
            print(f"Category '{new_cat.capitalize()}' created!")
        except sqlite3.IntegrityError:
            print("Category already exists.")

    # OPTION 2: ADD WORD
    elif choice == '2':
        print("\n === Add Word (Create) ===")
        cursor.execute("SELECT id, name FROM categories")
        cats = cursor.fetchall()
        for i, c in enumerate(cats, 1): print(f"{i}. {c[1].capitalize()}")
        
        c_choice = input("Select category number: ")
        if c_choice.isdigit() and 1 <= int(c_choice) <= len(cats):
            cat_id = cats[int(c_choice)-1][0]
            new_w = input("Enter new word: ").strip().lower()
            cursor.execute("INSERT INTO words (category_id, word) VALUES (?, ?)", (cat_id, new_w))
            conn.commit()
            print(f"Added '{new_w}'!")

    # OPTION 3: VIEW WORDS
    elif choice == '3':
        print("\n=== View Words (Read) ===")
        cursor.execute("""
            SELECT c.name, GROUP_CONCAT(w.word, ', ') 
            FROM categories c 
            LEFT JOIN words w ON c.id = w.category_id 
            GROUP BY c.name
        """)
        for cat, w_list in cursor.fetchall():
            print(f"{cat.capitalize()}: {w_list if w_list else 'Empty'}")

    elif choice == '4':
        print("\n=== Edit Word (Update) ===")
        cursor.execute("SELECT id, name FROM categories")
        cats = cursor.fetchall()
        for i, c in enumerate(cats, 1): print(f"{i}. {c[1].capitalize()}")
        c_choice = input("Category number: ")
        if c_choice.isdigit() and 1 <= int(c_choice) <= len(cats):
            cat_id = cats[int(c_choice)-1][0]
            cursor.execute("SELECT id, word FROM words WHERE category_id = ?", (cat_id,))
            word_rows = cursor.fetchall()
            for i, w in enumerate(word_rows, 1): print(f"{i}. {w[1]}")
            
            w_choice = input("Select word number to edit: ")
            if w_choice.isdigit() and 1 <= int(w_choice) <= len(word_rows):
                word_id = word_rows[int(w_choice)-1][0]
                new_val = input("New word value: ").strip().lower()
                cursor.execute("UPDATE words SET word = ? WHERE id = ?", (new_val, word_id))
                conn.commit()
                print("Updated!")


    # OPTION 5: REMOVE WORD (UPDATED DYNAMIC LOGIC)
    elif choice == '5':
        print("\n=== Remove Word (Delete) ===")
        cursor.execute("SELECT id, name FROM categories")
        cats = cursor.fetchall()
        for i, c in enumerate(cats, 1): print(f"{i}. {c[1].capitalize()}")
        c_choice = input("Category number: ")
        if c_choice.isdigit() and 1 <= int(c_choice) <= len(cats):
            cat_id = cats[int(c_choice)-1][0]
            cursor.execute("SELECT id, word FROM words WHERE category_id = ?", (cat_id,))
            word_rows = cursor.fetchall()
            for i, w in enumerate(word_rows, 1): print(f"{i}. {w[1]}")
            
            w_choice = input("Select word number to remove: ")
            if w_choice.isdigit() and 1 <= int(w_choice) <= len(word_rows):
                word_id = word_rows[int(w_choice)-1][0]
                cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
                conn.commit()
                print("Removed.")

    # OPTION 6: REMOVE Category (UPDATED DYNAMIC LOGIC)
    elif choice == '6':
        print("\n=== Remove Category (Delete) ===")
        cursor.execute("SELECT id, name FROM categories")
        cats = cursor.fetchall()
        for i, c in enumerate(cats, 1): print(f"{i}. {c[1].capitalize()}")
        c_choice = input("Select category number to DELETE: ")
        if c_choice.isdigit() and 1 <= int(c_choice) <= len(cats):
            cat_id = cats[int(c_choice)-1][0]
            cursor.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
            conn.commit()
            print("Category and all its words deleted.")

    conn.close()    

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
