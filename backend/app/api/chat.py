from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ask_question
from app.services.conversation_service import (
    create_conversation, add_message,
    get_conversation_history, get_all_conversations
)

router = APIRouter(prefix="/chat", tags=["chat"])

class QuestionRequest(BaseModel):
    question: str
    conversation_id: str = None

@router.post("/ask")
def ask(request: QuestionRequest):
    """Ask a question with conversation memory"""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Create new conversation if none provided
    conv_id = request.conversation_id
    if not conv_id:
        conv_id = create_conversation()
    
    # Get conversation history
    history = get_conversation_history(conv_id)
    
    # Get answer
    result = ask_question(request.question, history)
    
    # Save messages to conversation
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