import motor.motor_asyncio
from app.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.UltimateBot

def user_state_helper(state_user) -> dict:
    return {
        "id": str(state_user["_id"]),
        "user_id": state_user["user_id"],
        "username": state_user["username"],
        "state": state_user["state"],
    }