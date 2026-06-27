import uuid
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.db_models import UserDB

def hash_password(password: str) -> str:
    password_bytes = password[:72].encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    password_bytes = plain[:72].encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(db: Session, email: str, password: str) -> dict:
    """Register a new user"""
    existing = db.query(UserDB).filter(UserDB.email == email).first()
    if existing:
        return None
    
    user = UserDB(
        id=str(uuid.uuid4()),
        email=email,
        hashed_password=hash_password(password),
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}

def authenticate_user(db: Session, email: str, password: str) -> dict | None:
    """Verify email and password"""
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return {"id": user.id, "email": user.email}

def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT token"""
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": user_id, "email": email, "exp": expire}
    return jwt.encode(
        payload, settings.secret_key, algorithm=settings.algorithm
    )

def verify_token(token: str) -> dict | None:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None