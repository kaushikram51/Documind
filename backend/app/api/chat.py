from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.ai_service import ask_question
from app.services.database_service import (
    create_conversation, add_message, get_conversation_history
)

router = APIRouter(prefix="/chat", tags=["chat"])

class QuestionRequest(BaseModel):
    question: str
    conversation_id: str = None

    @validator("question")
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        if len(v) > 1000:
            raise ValueError("Question too long. Max 1000 characters.")
        return v.strip()

@router.post("/ask")
def ask(
    request: QuestionRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv_id = request.conversation_id
    if not conv_id:
        conv_id = create_conversation(db, current_user["id"])

    history = get_conversation_history(db, conv_id)

    try:
        result = ask_question(request.question, history)
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI service error")

    add_message(db, conv_id, "user", request.question)
    add_message(db, conv_id, "assistant", result["answer"])

    return {
        "conversation_id": conv_id,
        "answer": result["answer"],
        "sources": result["sources"]
    }