from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.document_service import (
    extract_text_from_pdf, chunk_text, generate_document_id
)
from app.services.vector_store import store_chunks
from app.services.database_service import (
    save_document, get_all_documents,
    get_document, delete_document
)

router = APIRouter(prefix="/documents", tags=["documents"])
MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    
    file_bytes = await file.read()
    
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 10MB")
    
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    
    try:
        text = extract_text_from_pdf(file_bytes)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read PDF")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")
    
    doc_id = generate_document_id(file.filename, text)
    existing = get_document(db, doc_id)
    if existing:
        raise HTTPException(status_code=409, detail="Document already uploaded")
    
    chunks = chunk_text(text)
    store_chunks(chunks, doc_id, file.filename)
    
    doc_data = {
        "id": doc_id,
        "filename": file.filename,
        "file_type": "pdf",
        "file_size": len(file_bytes),
        "chunk_count": len(chunks)
    }
    save_document(db, doc_data, current_user["id"])
    
    return {
        "message": "Document uploaded successfully",
        "document_id": doc_id,
        "chunks_created": len(chunks)
    }

@router.get("/")
def list_documents(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_documents(db, current_user["id"])

@router.get("/{doc_id}")
def get_single_document(
    doc_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{doc_id}")
def remove_document(
    doc_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_document(db, doc_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}