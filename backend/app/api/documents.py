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

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = ["application/pdf"]
MAX_QUESTION_LENGTH = 1000

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""

    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are supported."
        )

    # Read file
    file_bytes = await file.read()

    # Validate file size
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is 10MB."
        )

    # Validate file is not empty
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="File is empty."
        )

    # Extract text
    try:
        text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Could not read PDF. The file may be corrupted."
        )

    # Validate extracted text
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text found in PDF. The file may contain only images."
        )

    # Check for duplicate document
    doc_id = generate_document_id(file.filename, text)
    existing = get_document(doc_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Document '{file.filename}' has already been uploaded."
        )

    # Chunk and store
    chunks = chunk_text(text)
    store_chunks(chunks, doc_id, file.filename)

    # Save metadata
    doc = Document(
        id=doc_id,
        filename=file.filename,
        file_type="pdf",
        file_size=len(file_bytes),
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