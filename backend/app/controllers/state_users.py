# from http.client import HTTPException
from fastapi import APIRouter, HTTPException
# from app.models import MenuModel
from app.models import StateUserModel, UpdateUserModel, UpdateUserStateModel
from typing import List
from app.database import db, user_state_helper
from bson.objectid import ObjectId


router = APIRouter(
    prefix="/api/v1/state_users"
)

@router.get("/", response_description="List all users", response_model=List[StateUserModel])
async def list_users():
    state_users = await db["state_users"].find().to_list(1000)
    return state_users

# GET by id
@router.get("/{id}", response_description="Get a single user", response_model=StateUserModel)
async def show_user(id: str):
    state_user = await db["state_users"].find_one({"_id": ObjectId(id)})
    if state_user:
        return user_state_helper(state_user)

    raise HTTPException(status_code=404, detail=f"User {id} not found")


# GET by user_id
@router.get("/user_id/{user_id}", response_description="Get a single user", response_model=StateUserModel)
async def show_user_by_id(user_id: int):
    state_user = await db["state_users"].find_one({"user_id": user_id})
    if state_user:
        return user_state_helper(state_user)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


# GET by username
@router.get("/username/{username}", response_description="Get a user by username", response_model=StateUserModel)
async def show_user_by_username(username: str):
    state_user = await db["state_users"].find_one({"username": username})
    if state_user:
        return user_state_helper(state_user)

    raise HTTPException(status_code=404, detail=f"User {username} not found")


# ADD a new user
@router.post("/", response_description="Add a new user", response_model=StateUserModel)
async def add_user(state_user: StateUserModel):
    state_user = await db["state_users"].insert_one(state_user.dict())
    new_state_user = await db["state_users"].find_one({"_id": state_user.inserted_id})
    return user_state_helper(new_state_user)


# Delete user from database
@router.delete("/{id}", response_description="Delete user")
async def delete_user(id: str):
    delete_result = await db["state_users"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully!"}
    return {"message": "User not found"}


# Delete user by user_id
@router.delete("/user_id/{user_id}", response_description="Delete user by user_id")
async def delete_user_by_id(user_id: int):
    delete_result = await db["state_users"].delete_one({"user_id": user_id})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully!"}
    return {"message": "User not found"}


# Delete user by username
@router.delete("/username/{username}", response_description="Delete user by username")
async def delete_user_by_username(username: str):
    delete_result = await db["state_users"].delete_one({"username": username})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully!"}
    return {"message": "User not found"}


# Update user in database
@router.put("/{id}", response_description="Update user by id", response_model=UpdateUserModel)
async def update_user(id: str, state_user: UpdateUserModel):
    state_user = dict(state_user)
    update_result = await db["state_users"].update_one({"_id": ObjectId(id)}, {"$set": state_user})
    if update_result.modified_count == 1:
        return {"message": "User updated successfully!"}
    return {"message": "User not found"}

# Update user by user_id
@router.put("/user_id/{user_id}", response_description="Update user by user_id", response_model=UpdateUserModel)
async def update_user_by_id(user_id: int, state_user: UpdateUserModel):
    state_user = dict(state_user)
    update_result = await db["state_users"].update_one({"user_id": user_id}, {"$set": state_user})
    if update_result.modified_count == 1:
        return {"message": "User updated successfully!"}
    return {"message": "User not found"}

# Update user by username
@router.put("/username/{username}", response_description="Update user by username", response_model=UpdateUserModel)
async def update_user_by_username(username: str, state_user: UpdateUserModel):
    state_user = dict(state_user)
    update_result = await db["state_users"].update_one({"username": username}, {"$set": state_user})
    if update_result.modified_count == 1:
        return {"message": "User updated successfully!"}
    return {"message": "User not found"}

# Update state of user ode by uer_id
@router.put("/state/user_id/{user_id}", response_description="Update state of user by user_id")
async def update_state_user_by_id(user_id: int, state: str):
    update_result = await db["state_users"].update_one({"user_id": user_id}, {"$set": {"state": state}})
    if update_result.modified_count == 1:
        return {"message": "User updated successfully!"}
    return {"message": "User not found"}

# Update state of user ode by username
@router.put("/state/username/{username}", response_description="Update state of user by username")
async def update_state_user_by_username(username: str, state: str):
    update_result = await db["state_users"].update_one({"username": username}, {"$set": {"state": state}})
    if update_result.modified_count == 1:
        return {"message": "User updated successfully!"}
    return {"message": "User not found"}