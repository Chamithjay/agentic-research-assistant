import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pymongo.errors import ConnectionFailure

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("MONGO_DB_NAME")


class Database:
    """Database connection class to manage MongoDB client."""

    client: AsyncIOMotorClient = None
    db = None
    fs_bucket: AsyncIOMotorGridFSBucket = None


db_instance = Database()
fs_bucket: AsyncIOMotorGridFSBucket = None


async def connect_to_mongo():
    """Establish connection to MongoDB and initialize GridFS bucket."""
    global fs_bucket
    try:
        db_instance.client = AsyncIOMotorClient(MONGO_URI)
        db_instance.db = db_instance.client[DATABASE_NAME]
        db_instance.fs_bucket = AsyncIOMotorGridFSBucket(db_instance.db)
        await db_instance.db.command("ping")
        print("Connected to MongoDB!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")


async def close_mongo_connection():
    """Close the MongoDB connection."""
    if db_instance.client:
        db_instance.client.close()
        print("MongoDB connection closed.")
