import sqlite3

class DatabaseManager: # This class manages the SQLite database connection and operations
    def __init__(self, db_name='example.db'):
        self.db_name = db_name
        self.init_database()
    # This method initializes the database by creating necessary tables if they don't exist
    def init_database(self): 
        ''' Initialize the database and create tables if they don't exist '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Create posts table with id, user_id, title, content, and created_at fields, and a foreign key reference to users table
            cursor.execute(''' 
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
        
    # Update data in the database
    def update_user(self, user_id, name=None, email=None, age=None):
        """ Update user information in the database """
        with sqlite3.connect(self.db_name) as conn: # Connect to the database using a context manager to ensure proper resource management
            cursor = conn.cursor() # Create a cursor object to execute SQL commands
            fields = [] # List to hold the fields that need to be updated
            values = [] # List to hold the corresponding values for the fields that need to be updated
            if name: 
                fields.append("name = ?") # If a new name is provided, add it to the fields list with a placeholder for parameterized query 
                values.append(name)  # Add the new name value to the values list
            if email:
                fields.append("email = ?")
                values.append(email)
            if age is not None:
                fields.append("age = ?")
                values.append(age)
            values.append(user_id)
            sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"  # Construct the SQL query dynamically based on which fields are being updated, using parameterized queries to prevent SQL injection
            cursor.execute(sql, values)
            return cursor.rowcount > 0
        
    def update_post(self, post_id, title=None, content=None):
        """ Update post information in the database """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            if title:
                fields.append("title = ?")
                values.append(title)
            if content:
                fields.append("content = ?")
                values.append(content)
            values.append(post_id)
            sql = f"UPDATE posts SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(sql, values)
            return cursor.rowcount > 0
        
# Run on TERMINAL FUNCTION
def display_menu():
    """ Display the main menu options to the user """
    print("\n" +"=" *40)
    print("Welcome to Database Manager")
    print("="*40)
    print("1. Create User")
    print("2. View All Users")
    print("3. Create Post")
    print("4. View User Posts")
    print("5. Delete User")
    print("6. Update User")
    print("7. Update Post")
    print("8. Exit")
    print("="*40)

def main():
    """ Main function to run the database manager application """
    db_manager = DatabaseManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
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
                print("X Invalid age. Please enter a number.")        

        elif choice == '2':
            print("\n--- All Users ---")
            users = db_manager.get_all_users()
            for user in users:
                print(f"ID: {user[0]}")
                print(f"Name: {user[1]}")
                print(f"Email: {user[2]}")
                print(f"Age: {user[3]}")
                print(f"Created At: {user[4]}\n")
            else:
                print("No other users found.")

        elif choice == '3':
            print("\n--- Creating a new post ---")
            try:
                user_id = int(input("Enter user ID: "))
                title = input("Enter post title: ").strip()
                content = input("Enter post content: ").strip()
                post_id = db_manager.create_post(user_id, title, content)
                if post_id:
                    print(f"Post created with ID: {post_id}")
                else:
                    print("X Failed to create post.")
            except ValueError:
                print("X Invalid user ID. Please enter a number.")
        
        elif choice == '4':
            print("\n--- View User Posts ---")
            try:
                user_id = int(input("Enter user ID: ").strip())
                posts = db_manager.get_user_posts(user_id)
                if posts:
                    for post in posts:
                        print(f"ID: {post[0]} ")
                        print(f"Title: {post[1]}")
                        print(f"Content: {post[2]}")
                        print(f"Created At: {post[3]}")
                        print("-" * 20)
                else:
                    print("No posts found for this user.")
            except ValueError:
                print("X Invalid user ID. Please enter a number.")
        
        elif choice == '5':
            print("\n--- Delete User ---")
            try:
                user_id = int(input("Enter user ID to delete: ").strip())
                confirm = input(f"Are you sure you want to delete user with ID {user_id}? This will also delete all their posts. (y/n): ").strip().lower()
                if confirm == 'y':
                    if db_manager.delete_user(user_id):
                        print("User deleted successfully.")
                    else:
                        print("X Failed to delete user. User not found or deletion failed.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("X Invalid user ID. Please enter a number.")
        elif choice == '6':
            print("\n--- Update User ---")

            print("\n--- Existing Users In Database ---")
            users = db_manager.get_all_users()
            for user in users:
                print(f"ID: {user[0]}")
                print(f"Name: {user[1]}")
                print(f"Email: {user[2]}")
                print(f"Age: {user[3]}")
                print(f"Created At: {user[4]}\n")
            else:
                print("No users found.")
            
            try:
                user_id = int(input("Enter user ID to update: ").strip())
                name = input("Enter new name (leave blank to keep current): ").strip()
                email = input("Enter new email (leave blank to keep current): ").strip()
                age_input = input("Enter new age (leave blank to keep current): ").strip()
                age = int(age_input) if age_input else None
                # update the db_manager.update_user(user_id, name, email, age) based on user_id and provided fields
                confirm = input(f"Are you sure you want to update user ID {user_id} : {name}? (y/n): ").strip().lower()
                if confirm == 'y':
                    if db_manager.update_user(user_id, name, email, age):
                        print("User updated successfully.")
                    else:
                        print("X Failed to update user. User not found or update failed.")
                else:
                    print("Update cancelled.")
            except ValueError:
                print("X Invalid input. Please enter a number for user ID and age.") 

        elif choice == '7':
            print("\n--- Update Post ---")

            print("\n--- Existing Posts In Database ---")
            try:
                user_id = int(input("Enter user ID: ").strip())
                posts = db_manager.get_user_posts(user_id)
                if posts:
                    for post in posts:
                        print(f"ID: {post[0]} ")
                        print(f"Title: {post[1]}")
                        print(f"Content: {post[2]}")
                        print(f"Created At: {post[3]}")
                        print("-" * 20)
                else:
                    print("No posts found for this user.")
            except ValueError:
                print("X Invalid user ID. Please enter a number.")

            try:
                post_id = int(input("Enter post ID to update: ").strip())
                title = input("Enter new title (leave blank to keep current): ").strip()
                content = input("Enter new content (leave blank to keep current): ").strip()
                confirm = input(f"Are you sure you want to update post ID {post_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    if db_manager.update_post(post_id, title, content):
                        print("Post updated successfully.")
                    else:
                        print("X Failed to update post. Post not found or update failed.")
                else:
                    print("Update cancelled.")
            except ValueError:
                print("X Invalid input. Please enter a number for post ID.") 

        elif choice == '8':
            print("\n Goodbye! Exiting the application.")
            break

        else:
            print("Invalid choice. Please enter 1-8.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()


