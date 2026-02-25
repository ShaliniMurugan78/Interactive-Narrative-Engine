from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URI, MONGODB_DB_NAME

# MongoDB client instance
client = None
db = None

# Collections
stories_collection = None
sessions_collection = None
users_collection = None


async def connect_db():
    """Connect to MongoDB Atlas"""
    global client, db
    global stories_collection, sessions_collection, users_collection

    try:
        # Create async MongoDB client
        client = AsyncIOMotorClient(MONGODB_URI)

        # Select database
        db = client[MONGODB_DB_NAME]

        # Set up collections
        stories_collection  = db["stories"]
        sessions_collection = db["sessions"]
        users_collection    = db["users"]

        # Test the connection
        await client.admin.command("ping")
        print("✅ MongoDB connected successfully!")
        print(f"   → Database   : {MONGODB_DB_NAME}")
        print(f"   → Collections: stories, sessions, users")

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise e


async def disconnect_db():
    """Disconnect from MongoDB Atlas"""
    global client
    if client:
        client.close()
        print("✅ MongoDB disconnected successfully!")


def get_stories_collection():
    return stories_collection


def get_sessions_collection():
    return sessions_collection


def get_users_collection():
    return users_collection