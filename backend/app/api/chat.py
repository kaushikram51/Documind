from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from app.services.ai_service import ask_question
from app.services.conversation_service import (
    create_conversation, add_message,
    get_conversation_history, get_all_conversations
)

router = APIRouter(prefix="/chat", tags=["chat"])

MAX_QUESTION_LENGTH = 1000

class QuestionRequest(BaseModel):
    question: str
    conversation_id: str = None

    @validator("question")
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        if len(v) > MAX_QUESTION_LENGTH:
            raise ValueError(f"Question too long. Maximum {MAX_QUESTION_LENGTH} characters.")
        return v.strip()

@router.post("/ask")
def ask(request: QuestionRequest):
    """Ask a question with conversation memory"""

    # Validate conversation ID if provided
    if request.conversation_id:
        history = get_conversation_history(request.conversation_id)
        if history == []:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        conv_id = request.conversation_id
    else:
        conv_id = create_conversation()
        history = []

    # Get answer
    try:
        result = ask_question(request.question, history)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="AI service error. Please try again."
        )

    # Save messages
    add_message(conv_id, "user", request.question)
    add_message(conv_id, "assistant", result["answer"])

    return {
        "conversation_id": conv_id,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@router.get("/conversations")
def list_conversations():
    """List all conversations"""
    return get_all_conversations()

@router.get("/conversations/{conv_id}")
def get_conversation(conv_id: str):
    """Get full conversation history"""
    history = get_conversation_history(conv_id)
    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conv_id, "messages": history}