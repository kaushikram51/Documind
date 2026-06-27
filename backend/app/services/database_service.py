import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.db_models import DocumentDB, ConversationDB, MessageDB

# Document operations
def save_document(db: Session, doc_data: dict, owner_id: str):
    doc = DocumentDB(
        id=doc_data["id"],
        filename=doc_data["filename"],
        file_type=doc_data["file_type"],
        file_size=doc_data["file_size"],
        chunk_count=doc_data["chunk_count"],
        status="ready",
        upload_date=datetime.now(),
        owner_id=owner_id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_all_documents(db: Session, owner_id: str) -> list:
    docs = db.query(DocumentDB).filter(
        DocumentDB.owner_id == owner_id
    ).order_by(DocumentDB.upload_date.desc()).all()
    return [doc_to_dict(d) for d in docs]

def get_document(db: Session, doc_id: str) -> dict | None:
    doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    return doc_to_dict(doc) if doc else None

def delete_document(db: Session, doc_id: str, owner_id: str) -> bool:
    doc = db.query(DocumentDB).filter(
        DocumentDB.id == doc_id,
        DocumentDB.owner_id == owner_id
    ).first()
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True

def doc_to_dict(doc: DocumentDB) -> dict:
    return {
        "id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "file_size": doc.file_size,
        "chunk_count": doc.chunk_count,
        "status": doc.status,
        "upload_date": doc.upload_date.isoformat()
    }

# Conversation operations
def create_conversation(db: Session, owner_id: str) -> str:
    conv = ConversationDB(
        id=str(uuid.uuid4()),
        owner_id=owner_id,
        created_at=datetime.now()
    )
    db.add(conv)
    db.commit()
    return conv.id

def add_message(db: Session, conv_id: str, role: str, content: str):
    message = MessageDB(
        id=str(uuid.uuid4()),
        conversation_id=conv_id,
        role=role,
        content=content,
        timestamp=datetime.now()
    )
    db.add(message)
    db.commit()

def get_conversation_history(db: Session, conv_id: str) -> list[dict]:
    messages = db.query(MessageDB).filter(
        MessageDB.conversation_id == conv_id
    ).order_by(MessageDB.timestamp).all()
    return [{"role": m.role, "content": m.content} for m in messages]