import json
import os
import uuid
from datetime import datetime

CONVERSATIONS_FILE = "./conversations_db.json"

def _load_db() -> dict:
    if not os.path.exists(CONVERSATIONS_FILE):
        return {"conversations": {}}
    with open(CONVERSATIONS_FILE, "r") as f:
        return json.load(f)

def _save_db(data: dict):
    with open(CONVERSATIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_conversation() -> str:
    """Create a new conversation and return its ID"""
    db = _load_db()
    conv_id = str(uuid.uuid4())
    db["conversations"][conv_id] = {
        "id": conv_id,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }
    _save_db(db)
    return conv_id

def add_message(conv_id: str, role: str, content: str):
    """Add a message to a conversation"""
    db = _load_db()
    if conv_id not in db["conversations"]:
        return False
    db["conversations"][conv_id]["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    _save_db(db)
    return True

def get_conversation_history(conv_id: str) -> list[dict]:
    """Get all messages in a conversation"""
    db = _load_db()
    if conv_id not in db["conversations"]:
        return []
    messages = db["conversations"][conv_id]["messages"]
    return [{"role": m["role"], "content": m["content"]} for m in messages]

def get_all_conversations() -> list[dict]:
    """Get all conversations"""
    db = _load_db()
    convs = list(db["conversations"].values())
    return sorted(convs, key=lambda x: x["created_at"], reverse=True)