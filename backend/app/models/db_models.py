from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from app.core.database import Base

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class DocumentDB(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    status = Column(String, default="ready")
    upload_date = Column(DateTime, default=datetime.now)
    owner_id = Column(String, nullable=False)

class ConversationDB(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class MessageDB(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)