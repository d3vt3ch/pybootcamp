from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import sqlite3
from sqlite_lesson import DatabaseManager

app = FastAPI(title = "SQLITE Database API", version = "1.0.0")

# BASEMODEL

# pydantic model for request/response validation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    created_at: str

class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str
    
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

class PostResponseforUser(PostResponse):
    id: int
    title: str
    content: str
    created_at: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Initialize database manager
db = DatabaseManager()

@app.get("/")
async def root():
    return {"message" : "SQLITE DATABASE API" , "version" : "1.0.0"}

@app.post("/users/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user in the database."""
    try:
        user_id = db.create_user(user.name, user.email, user.age)
        if user_id:
            return {"message": "User created successfully", "user_id": user_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user. Email might already exist.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
@app.get("/users/", response_model=List[UserResponse])
async def get_all_users():
    """Get All Users from the database."""
    try:
        users = db.get_all_users()
        return [
            UserResponse(
                id=user[0],
                name=user[1],
                email=user[2],
                age=user[3],
                created_at=user[4]
            ) 
            for user in users
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a user by ID from the database."""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, age, created_at FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        return UserResponse(
            id=user[0],
            name=user[1],
            email=user[2],
            age=user[3],
            created_at=user[4]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
@app.post("/posts/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    """Create a now post"""
    try:
        # Check if user exists
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (post.user_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found. Cannot create post."
                ) 
        post_id = db.create_post(post.user_id, post.title, post.content)
        if post_id:
            return {"message": "Post created successfully", "post_id": post_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create post."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
@app.get("/users/{user_id}/posts/", response_model=List[PostResponseforUser])
async def get_user_posts(user_id: int):
    """Get all posts for a specific user."""
    try:
        #check if the user exists
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
        posts = db.get_user_posts(user_id)
        return [
            PostResponseforUser(
                id=post[0],
                title=post[1],
                content=post[2],
                created_at=post[3]
            ) 
            for post in posts
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
@app.get("/posts/", response_model=List[PostResponse])
async def get_all_posts():
    """ Get all posts """
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
            posts = cursor.fetchall()

        return [
            PostResponse(
                id=post[0],
                user_id=post[1],
                title=post[2],
                content=post[3],
                created_at=post[4]
            )
            for post in posts
        ] 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error:{str(e)}"
        )
    
@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id:int):
    """Delete a user and all their posts"""
    try:
        # Check if user exists
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        success = db.delete_user(user_id)
        if success:
            return{"message": "User deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete user"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id:int):
    """Delete a specific post"""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )
        return {"message" : "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=f"Internal server error: {str(e)}"
        )

@app.patch("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, user_data: UserUpdate):
    """Update user information partially."""
    # Convert Pydantic model to a dict, excluding fields that weren't sent
    update_fields = user_data.model_dump(exclude_unset=True)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Call your existing DatabaseManager method
    success = db.update_user(user_id, **update_fields)
    
    if success:
        return {"message": f"User {user_id} updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    
@app.patch("/posts/{post_id}", response_model=dict)
async def update_post(post_id: int, post_data: PostUpdate):
    """Update post information partially."""
    update_fields = post_data.model_dump(exclude_unset=True)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    success = db.update_post(post_id, **update_fields)
    
    if success:
        return {"message": f"Post {post_id} updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found or no changes made")
    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000)