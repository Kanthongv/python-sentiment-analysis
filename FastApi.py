from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Data model
class User(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: int
    name: str

# Sample data
# This is a list of users that we will use to simulate a database.
users: List[User] = [
    User(id=1, name="Alice"),
    User(id=2, name="Bob")
]

# GET a home page
@app.get("/")
def get_home():
    return "This is a home"

# GET all users
@app.get("/users", response_model=List[User])
def get_users():
    return users

# GET a specific user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    return {"error": "User not found"}

# POST to add a new user
@app.post("/users", response_model=User)
def add_user(user: User):
    users.append(user)
    return user

# PUT to update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = updated_user
            return updated_user
    return {"error": "User not found"}

# DELETE a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    users = [u for u in users if u.id != user_id]
    return {"message": "User deleted"}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    PORT = 8000
    uvicorn.run(app, host="0.0.0.0", port=PORT)