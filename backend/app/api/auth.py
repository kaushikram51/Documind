from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.auth_service import create_user, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest):
    """Register a new user"""
    if len(request.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters"
        )
    
    user = create_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    
    return {"message": "Account created successfully", "email": user["email"]}

@router.post("/login")
def login(request: LoginRequest):
    """Login and get access token"""
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    token = create_access_token(user["id"], user["email"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user["email"]
    }