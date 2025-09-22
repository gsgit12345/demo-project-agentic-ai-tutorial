from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.agentic_ai
sessions = db.sessions

# Start or fetch a session
user_id = "123"
session = sessions.find_one({"user_id": user_id})

if not session:
    # Create new session
    session_data = {
        "user_id": user_id,
        "session_id": "abc-456",
        "messages": [],
        "metadata": {"last_interaction": datetime.utcnow()}
    }
    sessions.insert_one(session_data)
else:
    session_data = session

# Add a new message to session
new_message = {"role": "user", "text": "What’s the weather today?"}
sessions.update_one(
    {"session_id": session_data["session_id"]},
    {"$push": {"messages": new_message}, "$set": {"metadata.last_interaction": datetime.utcnow()}}
)