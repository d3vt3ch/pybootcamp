# Create a API using FastAPI for CRUD database


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import Optional
import random

# --- DATABASE CONFIGURATION ---
DB_NAME = "hangman.db"

def init_db():
    """Initializes the database and populates default words if empty."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

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

# --- FASTAPI SETUP ---
app = FastAPI(title="Hangman Dictionary API")

# --- PYDANTIC MODELS ---
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class WordCreate(BaseModel):
    category_id: int
    word: str

class WordUpdate(BaseModel):
    word: str

class UserCreate(BaseModel):
    player_name: str
    wins: int = 0

class UserUpdate(BaseModel):
    new_player_name: Optional[str] = None
    wins: Optional[int] = None

# --- API ENDPOINTS ---

# 1. Create New Category (Create)
@app.post("/categories/", tags=["Categories"])
def create_category(category: CategoryCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category.name.lower().strip(),))
        conn.commit()
        return {"message": f"Category '{category.name}' created successfully!"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Category already exists.")
    finally:
        conn.close()

# 2. Add Word (Create)
@app.post("/words/", tags=["Words"])
def add_word(word_data: WordCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    try:
        cursor.execute("INSERT INTO words (category_id, word) VALUES (?, ?)", 
                       (word_data.category_id, word_data.word.lower().strip()))
        conn.commit()
        return {"message": f"Word '{word_data.word}' added successfully!"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid Category ID.")
    finally:
        conn.close()

# 3. View Words (Read)
@app.get("/words/", tags=["Words"])
def view_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id, c.name, GROUP_CONCAT(w.id || ':' || w.word, ', ') 
        FROM categories c 
        LEFT JOIN words w ON c.id = w.category_id 
        GROUP BY c.id, c.name
    """)
    
    # Format the data nicely into a dictionary mapping category to its words
    result = []
    for cat_id, cat_name, words_concat in cursor.fetchall():
        if words_concat:
            # Splits the concatenated string into a list of dicts with ID and Word
            word_list = [{"id": int(item.split(':')[0]), "word": item.split(':')[1]} for item in words_concat.split(', ')]
        else:
            word_list = []
        # Append a structured dictionary for each category
        result.append({
            "category_id": cat_id,
            "category_name": cat_name,
            "words": word_list
        })
            
    conn.close()
    return result

# 4. Edit Word (Update)
@app.put("/words/{word_id}", tags=["Words"])
def edit_word(word_id: int, word_data: WordUpdate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE words SET word = ? WHERE id = ?", (word_data.word.lower().strip(), word_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Word not found.")
        
    conn.commit()
    conn.close()
    return {"message": "Word updated successfully."}

# 5. Remove Word (Delete)
@app.delete("/words/{word_id}", tags=["Words"])
def remove_word(word_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Word not found.")
        
    conn.commit()
    conn.close()
    return {"message": "Word deleted successfully."}

# 8. Update the category 
# Update Category (Update)
@app.put("/categories/{category_id}", tags=["Categories"])
def update_category(category_id: int, category_data: CategoryUpdate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Clean the input to match your terminal logic
    new_name = category_data.name.lower().strip()
    
    try:
        cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (new_name, category_id))
        
        # Check if the category actually existed
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Category not found.")
            
        conn.commit()
        return {"message": f"Category renamed to '{new_name.capitalize()}' successfully!"}
        
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="A category with that name already exists.")
    finally:
        conn.close()

# 6. Remove Category (Delete)
@app.delete("/categories/{category_id}", tags=["Categories"])
def remove_category(category_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON") # Crucial for cascading deletes
    
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found.")
        
    conn.commit()
    conn.close()
    return {"message": "Category and all associated words deleted successfully."}

#7. View Categories (Read)
@app.get("/categories/", tags=["Categories"])
def view_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM categories")
    # Format the result into a clean list of dictionaries
    categories = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return categories




# --- USER (SCORE) ENDPOINTS ---

# 1. Create User (Create)
@app.post("/users/", tags=["Users"])
def create_user(user: UserCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # We use capitalize() to keep naming consistent with your terminal game logic
        clean_name = user.player_name.strip().capitalize()
        cursor.execute("INSERT INTO scores (player_name, wins) VALUES (?, ?)", (clean_name, user.wins))
        conn.commit()
        return {"message": f"User '{clean_name}' created with {user.wins} wins!"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists.")
    finally:
        conn.close()

# 2. View Users & Points (Read)
@app.get("/users/", tags=["Users"])
def view_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ordering by wins descending to act as a leaderboard
    cursor.execute("SELECT player_name, wins FROM scores ORDER BY wins DESC")
    
    # Format the result into a clean list of dictionaries
    users = [{"player_name": row[0], "wins": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return users

# 3. Update User Name & Points (Update)
@app.put("/users/{player_name}", tags=["Users"])
def update_user(player_name: str, update_data: UserUpdate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # First, verify the user exists and get their current data
    clean_target_name = player_name.strip().capitalize()
    cursor.execute("SELECT player_name, wins FROM scores WHERE player_name = ?", (clean_target_name,))
    current_user = cursor.fetchone()
    
    if not current_user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found.")
        
    # Determine what is being updated (fallback to current values if not provided)
    new_name = update_data.new_player_name.strip().capitalize() if update_data.new_player_name else current_user[0]
    new_wins = update_data.wins if update_data.wins is not None else current_user[1]
    
    try:
        cursor.execute("""
            UPDATE scores 
            SET player_name = ?, wins = ? 
            WHERE player_name = ?
        """, (new_name, new_wins, clean_target_name))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="A user with that new name already exists.")
    finally:
        conn.close()
        
    return {"message": f"User updated successfully.", "current_state": {"player_name": new_name, "wins": new_wins}}

# 4. Delete User (Delete)
@app.delete("/users/{player_name}", tags=["Users"])
def delete_user(player_name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    clean_target_name = player_name.strip().capitalize()
    cursor.execute("DELETE FROM scores WHERE player_name = ?", (clean_target_name,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found.")
        
    conn.commit()
    conn.close()
    return {"message": f"User '{clean_target_name}' deleted successfully."}

@app.get("/game/word/{category_id}", tags=["Game"])
def get_random_word(category_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT word FROM words WHERE category_id = ?",
        (category_id,)
    )
    words = cursor.fetchall()

    if not words:
        conn.close()
        raise HTTPException(status_code=404, detail="No words found for this category.")

    # Pick random word
    chosen_word = random.choice(words)[0]

    conn.close()

    return {
        "category_id": category_id,
        "word": chosen_word
    }   

@app.post("/game/win", tags=["Game"])
def record_win(player_name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    clean_name = player_name.strip().capitalize()

    cursor.execute("""
        INSERT INTO scores (player_name, wins)
        VALUES (?, 1)
        ON CONFLICT(player_name)
        DO UPDATE SET wins = wins + 1
    """, (clean_name,))

    conn.commit()
    conn.close()

    return {"message": f"{clean_name} win recorded!"}