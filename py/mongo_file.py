from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

mongo_uri = os.getenv("MONGODB_ATLAS_CLUSTER_URI") # Get MongoDB URI from environment variable

class DatabaseManager:
    def __init__(self, db_name='example_db', connection_string=mongo_uri):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.users_collection = self.db.users
        self.posts_collection = self.db.posts
        self.init_database()

    def init_database(self):
        """Initialize database with collections and indexed"""
        # Create unique index on email for users
        self.users_collection.create_index("email", unique=True)
        #create index on user_id for posts for better query performance
        self.posts_collection.create_index("user_id")
        
    def create_user(self, name, email, age):
        """Create a new user in the database"""
        try: 
            user_doc = {
                "name": name,
                "email": email,
                "age": age,
                "created_at": datetime.now()
            }
            result = self.users_collection.insert_one(user_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
            

    def create_post(self, user_id, title, content):
        """Create a new post for a user"""
        try:
            # Convert string user_id to ObjectId if its a valid ObjectId string
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id  # If it's not a valid ObjectId, use it as is (could be a string or other type)    
            
            post_doc = {
                "user_id": user_object_id,
                "title": title,
                "content": content,
                "created_at": datetime.now()
                }
            result = self.posts_collection.insert_one(post_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating post: {e}")
            return None
        
    def get_user_posts(self):
        """ Get all users """
        try:
            users = list(self.users_collection.find())
            # Convert ObjectId to string for display
            for user in users:
                user['_id'] = str(user['_id'])
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        
    def get_posts_by_user(self, user_id):
        """ Get all posts for a specific user """
        try:
            # Convert string user_id to ObjectId if its a valid ObjectId string
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id  # If it's not a valid ObjectId, use it as is (could be a string or other type)    
            
            posts = list(self.posts_collection.find(
                {"user_id": user_object_id}
            ).sort("created_at", -1))

            # Convert ObjectId to string for display
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])  # Convert user_id to string for display
            return posts
        
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []
        
    def delete_user(self, user_id):
        """Delete a user and their posts"""
        try:
            # Convert string user_id to ObjectId if its a valid ObjectId string
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id  # If it's not a valid ObjectId, use it as is (could be a string or other type)    
            
            # Delete the user first
            self.posts_collection.delete_many({"user_id": user_object_id})
            # Delete the user's posts
            result = self.users_collection.delete_one({"_id": user_object_id})
            return result.deleted_count > 0
            print(f"User {user_id} and their posts have been deleted.")
        except Exception as e:
            print(f"Error deleting user: {e}")  
            return False
        
    def close_connection(self):
        """Close the MongoDB connection"""
        self.client.close()

def display_menu():
    """ Display the main menu options to the user """
    print("\n" + "="*40)
    print("          Database Manager Menu")
    print("="*40)
    print("1. Create User")
    print("2. View All Users")
    print("3. Create Post")
    print("4. View Posts by User")
    print("5. Delete User")
    print("6. Exit")
    print("="*40)

def main():
    """ Main intereactive CLI function """
    try:
        db = DatabaseManager()
        print(" Connected to MongoDB Atlas Cluster successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas Cluster: {e}")
        print(" Make sure MongoDB is running on localhost:27017")
        return
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            print("\n--- Creating a new user ---")
            name = input("Enter user name: ").strip()
            email = input("Enter user email: ").strip()
            try:
                age = int(input("Enter user age: "))
                user_id = db.create_user(name, email, age)
                if user_id:
                    print(f"User created successfully! with ID: {user_id}")
                else:
                    print("Failed to create user. Please check the details and try again.")
            except ValueError:
                print("Invalid age. Please enter a number for age.")
        
        elif choice == '2':
            print("\n--- All Users ---")
            users = db.get_user_posts()
            if users:
                for user in users:
                    print(f"ID: {user['_id']} | Name: {user['name']} | Email: {user['email']} | Age: {user['age']}")
            else:
                print("No users found. Please create a user first.")

        elif choice == '3':
            print("\n--- Creating a new post ---")
            user_id = input("Enter user ID: ").strip()
            title = input("Enter post title: ").strip()
            content = input("Enter post content: ").strip()
            post_id = db.create_post(user_id, title, content)
            if post_id:
                print(f"Post created successfully! with ID: {post_id}")
            else:
                print("Failed to create post. Please check the details and try again.")

        elif choice == '4':
            print("\n--- View Posts by User ---")
            user_id = input("Enter user ID to view their posts: ").strip()
            posts = db.get_posts_by_user(user_id)
            if posts:
                for post in posts:
                    print(f"ID: {post['_id']}")
                    print(f"Title: {post['title']}")
                    print(f"Content: {post['content']}"), 
                    print(f"Created At: {post['created_at']}")
                    print("-"*30)
            else:
                print("No posts found for this user.")
                 
        elif choice == '5':
            print("\n--- Delete User ---")
            user_id = input("Enter user ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete user with ID {user_id} and all their posts? (y/N): ").strip().lower()
            if confirm == 'y':
                if db.delete_user(user_id):
                    print(f"User with ID {user_id} and their posts have been deleted.")
                else:
                    print("Failed to delete user. Please check the user ID and try again.")
            else:
                print("Deletion cancelled.")

        elif choice == '6':
            print("\n Closing database connection... ")
            db.close_connection()      
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()