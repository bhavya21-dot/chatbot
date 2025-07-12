import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_DB_URL = os.getenv("DATABASE_URL")
DB_NAME = os.getenv("DB_NAME", "rewear_db") 

client = None
db = None

def connect_db():
    global client, db

    if client:
        try:
            client.admin.command('ping')
            print("MongoDB client already connected and connection is alive.")
            db = client[DB_NAME]
            return
        except Exception as e:
            print(f"Existing MongoDB connection found but not alive. Reconnecting. Error: {e}")
            client = None
            db = None

    try:

        client = AsyncIOMotorClient(MONGO_DB_URL, server_api=ServerApi('1'))
        
        client.admin.command('ping') 
        
        db = client[DB_NAME]
        print(f"Successfully connected to MongoDB: {DB_NAME}")

        db.users.create_index("email", unique=True)
        db.clothing_items.create_index("user_id")
        db.clothing_items.create_index([("status", 1), ("posted_date", -1)])

        print("MongoDB indexes created/ensured.")

    except Exception as e:
        print(f"Error connecting to MongoDB or creating indexes: {e}")


def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")

connect_db()

def get_database():
    
    if db is None:
        connect_db()
        if db is None:
            raise Exception("Failed to get MongoDB database instance. Check connection and environment variables.")
    return db