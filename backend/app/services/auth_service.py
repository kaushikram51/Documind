import json
import os
import uuid
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings

USERS_FILE = "./users_db.json"

def _load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {"users": {}}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save_users(data: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password[:72].encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    password_bytes = plain[:72].encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(email: str, password: str) -> dict:
    """Register a new user"""
    db = _load_users()
    
    # Check if user exists
    for user in db["users"].values():
        if user["email"] == email:
            return None
    
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": email,
        "hashed_password": hash_password(password),
        "created_at": datetime.now().isoformat()
    }
    db["users"][user_id] = user
    _save_users(db)
    return {"id": user_id, "email": email}

def authenticate_user(email: str, password: str) -> dict | None:
    """Verify email and password"""
    db = _load_users()
    for user in db["users"].values():
        if user["email"] == email:
            if verify_password(password, user["hashed_password"]):
                return user
    return None

def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT token"""
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire
    }
    return jwt.encode(
        payload, settings.secret_key, algorithm=settings.algorithm
    )

def verify_token(token: str) -> dict | None:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None