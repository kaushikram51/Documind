import hashlib
from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file"""
    pdf_reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    
    return chunks

def generate_document_id(filename: str, content: str) -> str:
    """Generate a unique ID for a document"""
    hash_input = filename + content[:100]
    return hashlib.md5(hash_input.encode()).hexdigest()