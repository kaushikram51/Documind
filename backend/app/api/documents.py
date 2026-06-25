from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from app.services.document_service import (
    extract_text_from_pdf, chunk_text, generate_document_id
)
from app.services.vector_store import store_chunks
from app.services.database_service import (
    save_document, get_all_documents, 
    get_document, delete_document
)
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    
    # Read file
    file_bytes = await file.read()
    file_size = len(file_bytes)
    
    # Extract text
    text = extract_text_from_pdf(file_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
    
    # Generate ID and chunk
    doc_id = generate_document_id(file.filename, text)
    chunks = chunk_text(text)
    
    # Store in vector DB
    store_chunks(chunks, doc_id, file.filename)
    
    # Save metadata
    doc = Document(
        id=doc_id,
        filename=file.filename,
        file_type="pdf",
        file_size=file_size,
        chunk_count=len(chunks),
        status="ready",
        upload_date=datetime.now()
    )
    save_document(doc)
    
    return {
        "message": "Document uploaded successfully",
        "document_id": doc_id,
        "chunks_created": len(chunks)
    }

@router.get("/")
def list_documents():
    """List all uploaded documents"""
    return get_all_documents()

@router.get("/{doc_id}")
def get_single_document(doc_id: str):
    """Get a single document"""
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{doc_id}")
def remove_document(doc_id: str):
    """Delete a document"""
    success = delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}