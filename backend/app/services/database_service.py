import json
import os
from datetime import datetime
from app.models.document import Document

DB_FILE = "./documents_db.json"

def _load_db() -> dict:
    """Load database from JSON file"""
    if not os.path.exists(DB_FILE):
        return {"documents": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def _save_db(data: dict):
    """Save database to JSON file"""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_document(doc: Document):
    """Save document metadata"""
    db = _load_db()
    db["documents"][doc.id] = doc.to_dict()
    _save_db(db)

def get_all_documents() -> list[dict]:
    """Get all documents"""
    db = _load_db()
    docs = list(db["documents"].values())
    return sorted(docs, key=lambda x: x["upload_date"], reverse=True)

def get_document(doc_id: str) -> dict | None:
    """Get a single document by ID"""
    db = _load_db()
    return db["documents"].get(doc_id)

def delete_document(doc_id: str) -> bool:
    """Delete a document by ID"""
    db = _load_db()
    if doc_id in db["documents"]:
        del db["documents"][doc_id]
        _save_db(db)
        return True
    return False