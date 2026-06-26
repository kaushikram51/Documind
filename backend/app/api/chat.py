from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ask_question

router = APIRouter(prefix="/chat", tags=["chat"])

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask(request: QuestionRequest):
    """Ask a question about uploaded documents"""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = ask_question(request.question)
    return result