"""
MongoDB Atlas Database Connection & Helper Functions
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
DB_NAME = os.getenv("MONGODB_DB_NAME", "food_quality_db")

_mongo_client = None
_mongo_db = None

def get_mongo_db():
    """
    Returns the MongoDB database instance if MONGODB_URI is set and connected,
    otherwise returns None.
    """
    global _mongo_client, _mongo_db
    if not MONGODB_URI:
        return None

    if _mongo_db is None:
        try:
            from pymongo import MongoClient
            _mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=4000)
            # Test connection
            _mongo_client.admin.command('ping')
            _mongo_db = _mongo_client[DB_NAME]
            print(f"[MongoDB Atlas] Successfully connected to database '{DB_NAME}'!")
        except Exception as err:
            print(f"[MongoDB Atlas] Connection failed ({err}). Falling back to SQLite.")
            _mongo_db = None

    return _mongo_db

def is_mongo_connected() -> bool:
    return get_mongo_db() is not None

def save_mongo_scan(record: dict) -> str:
    """Inserts a scan record into MongoDB Atlas 'scan_history' collection."""
    db = get_mongo_db()
    if db is None:
        return None
    try:
        col = db["scan_history"]
        doc = record.copy()
        if "created_at" not in doc or not doc["created_at"]:
            doc["created_at"] = datetime.utcnow()
        res = col.insert_one(doc)
        return str(res.inserted_id)
    except Exception as e:
        print(f"[MongoDB Atlas] Error inserting document: {e}")
        return None

def get_mongo_history(limit: int = 50) -> list:
    """Retrieves scan history from MongoDB Atlas."""
    db = get_mongo_db()
    if db is None:
        return []
    try:
        col = db["scan_history"]
        cursor = col.find().sort("created_at", -1).limit(limit)
        results = []
        for doc in cursor:
            doc_id = str(doc.get("_id", ""))
            doc["id"] = doc_id
            doc.pop("_id", None)
            results.append(doc)
        return results
    except Exception as e:
        print(f"[MongoDB Atlas] Error retrieving history: {e}")
        return []
