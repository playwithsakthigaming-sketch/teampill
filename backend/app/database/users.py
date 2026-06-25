from datetime import UTC, datetime
from bson import ObjectId

from app.database.mongodb import db

collection = db.users


async def create_user(user: dict):
    user["created_at"] = datetime.now(UTC)
    user["updated_at"] = datetime.now(UTC)

    result = await collection.insert_one(user)

    return str(result.inserted_id)


async def get_user_by_email(email: str):
    return await collection.find_one({"email": email})


async def get_user_by_id(user_id: str):
    return await collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )


async def get_user_by_discord(discord_id: str):
    return await collection.find_one(
        {
            "discord_id": discord_id
        }
    )


async def update_refresh_token(user_id: str, token: str):

    await collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": {
                "refresh_token": token,
                "updated_at": datetime.now(UTC)
            }
        }
    )


async def clear_refresh_token(user_id: str):

    await collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$unset": {
                "refresh_token": ""
            }
        }
    )
