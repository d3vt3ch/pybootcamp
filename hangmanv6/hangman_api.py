# Update Authentication layer with password hashing
# Admin protection as root

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import Optional
import random
import bcrypt

# --- HASHING UTILITIES (NEW FOR PYTHON 3.13) ---
def hash_password(password: str):
    # Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Return as string to store in DB
    return hashed.decode('utf-8')

def verify_password(plain_password, hashed_password):
    # Convert both to bytes for comparison
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

# --- DATABASE CONFIGURATION ---
DB_NAME = "hangman.db"

def init_db():
    """Initializes the database and populates default words if empty."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # NEW: Table for authentication and roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'player' 
        )
    """)

    # Keep existing tables (categories, words, scores)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

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
            hint TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            player_name TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0
        )
    """)

    cursor.execute("PRAGMA table_info(words)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "hint" not in columns:
        cursor.execute("ALTER TABLE words ADD COLUMN hint TEXT")
        cursor.execute("SELECT id, word FROM words WHERE hint IS NULL")

        for word_id, word in cursor.fetchall():
            hint = f"A word related to {word}"  # simple fallback
            cursor.execute("UPDATE words SET hint = ? WHERE id = ?", (hint, word_id))

        conn.commit()
        conn.close()


    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_words = {
            "fruits": [
                ("apple", "Sweet fruit, usually red or green"),
                ("banana", "Long yellow fruit"),
                ("cherry", "Small red fruit"),
                ("date", "Sweet brown fruit often from Middle East"),
                ("fig", "Soft fruit with many seeds inside"),
                ("grape", "Small round fruit, used for wine")
            ],
            "animals": [
                ("cat", "Small pet that says meow"),
                ("dog", "Man’s best friend"),
                ("elephant", "Large animal with trunk"),
                ("giraffe", "Animal with long neck"),
                ("lion", "King of the jungle"),
                ("tiger", "Striped big cat")
            ],
            "countries": [
                ("usa", "Country in North America"),
                ("canada", "Cold country above USA"),
                ("brazil", "Famous for football"),
                ("india", "Second most populous country"),
                ("china", "Most populous country"),
                ("australia", "Country with kangaroo")
            ]
        }

        for cat, word_list in default_words.items():
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
            cat_id = cursor.lastrowid

            for w, hint in word_list:
                cursor.execute(
                    "INSERT INTO words (category_id, word, hint) VALUES (?, ?, ?)",
                    (cat_id, w, hint)
                )

        
    
    conn.commit()
    conn.close()



# Initialize DB at startup
init_db()

# --- FASTAPI SETUP ---
app = FastAPI(title="Hangman Dictionary API")

# --- PYDANTIC MODELS ---

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: str = "player"  # Default role

class UserLogin(BaseModel):
    username: str
    password: str


class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class WordCreate(BaseModel):
    category_id: int
    word: str
    hint: str   # NEW

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

#2. View Categories (Read)
@app.get("/categories/", tags=["Categories"])
def view_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM categories")
    # Format the result into a clean list of dictionaries
    categories = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return categories

# 3. Update the category 
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

# 4. Remove Category (Delete)
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

# 5. Add Word (Create)
@app.post("/words/", tags=["Words"])
def add_word(word_data: WordCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    try:
        cursor.execute(
        "INSERT INTO words (category_id, word, hint) VALUES (?, ?, ?)",
        (word_data.category_id, word_data.word.lower().strip(), word_data.hint)
        )
        conn.commit()
        return {"message": f"Word '{word_data.word}' added successfully!"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid Category ID.")
    finally:
        conn.close()

# 6. View Words (Read)
@app.get("/words/", tags=["Words"])
def view_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id, c.name, w.id, w.word, w.hint
        FROM categories c
        LEFT JOIN words w ON c.id = w.category_id
        ORDER BY c.id
    """)
    
    
    # Format the data nicely into a dictionary mapping category to its words
    result = {}
    for cat_id, cat_name, word_id, word, hint in cursor.fetchall():
        if cat_id not in result:
            result[cat_id] = {
                "category_id": cat_id,
                "category_name": cat_name,
                "words": []
            }

        if word_id:
            result[cat_id]["words"].append({
                "id": word_id,
                "word": word,
                "hint": hint
            })

    conn.close()
    return list(result.values())
    
# 7. Edit Word (Update)
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

# 8. Remove Word (Delete)
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

# --- AUTH ENDPOINTS ---

# --- AUTH ENDPOINTS (ADD THIS ONE) ---

@app.get("/auth/super-admin", tags=["Auth"])
def get_super_admin():
    """Identifies the first user ever registered (the Creator)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # In SQLite, the first row inserted is the one with the earliest 'rowid'
    cursor.execute("SELECT username FROM users ORDER BY rowid ASC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return {"username": result[0] if result else None}

@app.get("/auth/accounts", tags=["Auth"])
def get_all_accounts():
    """Returns a list of all registered accounts and their roles."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We select username, email, and role (excluding passwords for safety)
    cursor.execute("SELECT username, email, role FROM users")
    accounts = [{"username": row[0], "email": row[1], "role": row[2]} for row in cursor.fetchall()]
    
    conn.close()
    return accounts

@app.post("/auth/register", tags=["Auth"])
def register_user(user: UserRegister):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Check if any users exist in the database yet
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        # Bootstrap logic: First user is admin, everyone else is a player
        assigned_role = "admin" if user_count == 0 else "player"

        # HASH THE PASSWORD HERE
        hashed_pwd = hash_password(user.password)

        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", 
            (user.username.strip(), user.email.strip().lower(), hashed_pwd, assigned_role)
        )
        conn.commit()
        return {"message": f"User '{user.username}' registered successfully as {assigned_role}!"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or Email already exists.")
    finally:
        conn.close()

@app.post("/auth/login", tags=["Auth"])
def login_user(user: UserLogin):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Only fetch by username first
    cursor.execute("SELECT username, password, role FROM users WHERE username = ?", (user.username.strip(),))
    result = cursor.fetchone()
    conn.close()

    # Check if user exists AND password matches the hash
    if result and verify_password(user.password, result[1]):
        return {
            "message": "Login successful!",
            "username": result[0],
            "role": result[2]
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

# Helper to check if a user is the Super Admin
def is_super_admin(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY rowid ASC LIMIT 1")
    first_user = cursor.fetchone()
    conn.close()
    return first_user and first_user[0] == username

@app.put("/auth/demote/{target_username}", tags=["Auth"])
def demote_user(target_username: str):
    if is_super_admin(target_username):
        raise HTTPException(status_code=403, detail="The Super Admin cannot be demoted.")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Change role back to player
    cursor.execute("UPDATE users SET role = 'player' WHERE username = ?", (target_username,))
    return {"message": f"User '{target_username}' has been demoted."}

@app.delete("/auth/accounts/{username}", tags=["Auth"])
def delete_account(username: str):
    if is_super_admin(username):
        raise HTTPException(status_code=403, detail="The Super Admin account cannot be deleted.")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Delete from the authentication table
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Account not found.")
        
    conn.commit()
    conn.close()
    return {"message": f"Account '{username}' has been permanently deleted."}

@app.put("/auth/reset-password/{username}", tags=["Auth"])
def reset_password(username: str, new_data: UserLogin): # Using UserLogin model for username/password
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    hashed_pwd = hash_password(new_data.password)
    
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_pwd, username))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found.")
        
    conn.commit()
    conn.close()
    return {"message": f"Password for '{username}' has been reset successfully."}

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

# Random word
@app.get("/game/word/{category_id}", tags=["Game"])
def get_random_word(category_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT word, hint FROM words WHERE category_id = ?",
        (category_id,)
    )
    words = cursor.fetchall()

    if not words:
        conn.close()
        raise HTTPException(status_code=404, detail="No words found for this category.")

    # Pick random word
    chosen_word, hint = random.choice(words)

    conn.close()

    return {
        "category_id": category_id,
        "word": chosen_word,
        "hint": hint
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

@app.put("/auth/promote/{target_username}", tags=["Auth"])
def promote_user(target_username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", (target_username,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found.")
        
    conn.commit()
    conn.close()
    return {"message": f"User '{target_username}' has been promoted to Admin."}    

# --- GAME ENDPOINTS (ADD THIS) ---

@app.delete("/game/reset-scores", tags=["Game"])
def reset_scores():
    """Wipes all data from the scores table. Admin only (enforced by frontend)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM scores")
        conn.commit()
        return {"message": "Scoreboard has been reset successfully."}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()