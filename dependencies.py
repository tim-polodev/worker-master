from pymongo.database import Database

from config.database import db_mongo


def get_db() -> Database:
    """Dependency that provides the database instance."""
    if db_mongo.db is None:
        # This handles cases where the route might be called
        # before the lifespan context has initialized the connection
        db_mongo.connect()
    return db_mongo.db
