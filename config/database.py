from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import settings

MONGO_URI = f"mongodb://{settings.MONGO_DB_USER}:{settings.MONGO_DB_PASSWORD}@{settings.MONGO_DB_HOST}:{settings.MONGO_DB_PORT}"  # noqa: E501


class DBMongo:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self, uri=MONGO_URI, db_name=settings.MONGO_DB_NAME):
        """Connects to MongoDB and selects a database."""
        try:
            self.client = MongoClient(uri)
            self.client.admin.command("ping")  # Verify connection
            self.db = self.client[db_name]
            print("Successfully connected to MongoDB. ✅")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            # Handle the error appropriately (e.g., exit the app)
            raise "Could not connect to MongoDB."

    def close(self):
        """Closes the MongoDB connection."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")


# Create a single instance of the database connection manager
db_mongo = DBMongo()
