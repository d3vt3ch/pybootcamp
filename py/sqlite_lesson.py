import sqlite3

class DatabaseManager: # This class manages the SQLite database connection and operations
    def __init__(self, db_name='example.db'):
        self.db_name = db_name
        self.init_database()

    def init_database(self): # This method initializes the database by creating necessary tables if they don't exist
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute(''' # Create users table with id, name, email, age, and created_at fields
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute(''' # Create posts table with id, user_id, title, content, and created_at fields, and a foreign key reference to users table
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')

    def create_user(self, name, email, age):
        """ Create a new user in the database """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (name, email, age)
                    VALUES (?, ?, ?)
                ''', (name, email, age))
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
    
    def create_post(self, user_id, title, content):
        """ Create a new post for a user in the database """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO posts (user_id, title, content)
                VALUES (?, ?, ?)
            ''', (user_id, title, content))
            return cursor.lastrowid
    
    # Read data from the database
    def get_all_users(self):
        """ Retrieve all users from the database """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            return cursor.fetchall()
    
    def get_user_posts(self, user_id):
        """ Retrieve all posts for a specific user from the database """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT p.id, p.title, p.content, p.created_at
                           FROM posts p
                           WHERE p.user_id = ?
                           ORDER BY p.created_at DESC
                       ''', (user_id,))
            return cursor.fetchall()
        
    # Delete data from the database

    def delete_user(self, user_id):
        """ Delete a user and their posts from the database """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM posts WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            return cursor.rowcount > 0
        
# Run on TERMINAL FUNCTION
def display_menu():
    """ Display the main menu options to the user """
    print("\n" +"=" *40)
    print("Welcome to Database Manager")
    print("="*40)
    print("1. Create User")
    print("2. Create Post")
    print("3. View All Users")
    print("4. View User Posts")
    print("5. Delete User")
    print("6. Exit")
    print("="*40)

def main():
    """ Main function to run the database manager application """
    db_manager = DatabaseManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            print("\n--- Creating a new user ---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            try:
                age = int(input("Enter age: ").strip())
                user_id = db_manager.create_user(name, email, age)
                if user_id:
                    print(f"User created successfully! ID: {user_id}")
                else:
                    print("Failed to create user.")
            except ValueError:
                print("Invalid age. Please enter a number.")        


        elif choice == '2':
            user_id = int(input("Enter user ID: "))
            title = input("Enter post title: ")
            content = input("Enter post content: ")
            post_id = db_manager.create_post(user_id, title, content)
            print(f"Post created with ID: {post_id}")
        
        elif choice == '3':
            users = db_manager.get_all_users()
            for user in users:
                print(user)
        
        elif choice == '4':
            user_id = int(input("Enter user ID: "))
            posts = db_manager.get_user_posts(user_id)
            for post in posts:
                print(post)
        
        elif choice == '5':
            user_id = int(input("Enter user ID to delete: "))
            if db_manager.delete_user(user_id):
                print("User deleted successfully.")
            else:
                print("User not found.")
        
        elif choice == '6':
            print("Exiting the application.")
            break
        
        else:
            print("Invalid choice. Please try again.")
