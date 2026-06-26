from groq import Groq
from app.core.config import settings
from app.services.vector_store import search_similar_chunks

client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are DocuMind, a helpful AI assistant that answers 
questions based on uploaded documents.

IMPORTANT RULES:
1. Answer ONLY using the context provided below
2. If the answer is not in the context, say "I don't have enough information in the uploaded documents to answer this"
3. Always mention which document your answer came from
4. Be concise and clear

Context from uploaded documents:
{context}"""

def format_context(chunks: list[dict]) -> str:
    """Format chunks into readable context"""
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source: {chunk['filename']}, Chunk {chunk['chunk_index']}]\n{chunk['content']}"
        )
    return "\n\n".join(context_parts)

def ask_question(question: str) -> dict:
    """Ask a question and get an AI answer with citations"""
    
    # Step 1 — Find relevant chunks
    chunks = search_similar_chunks(question, n_results=3)
    
    if not chunks:
        return {
            "answer": "No documents found. Please upload a document first.",
            "sources": []
        }
    
    # Step 2 — Format context
    context = format_context(chunks)
    
    # Step 3 — Ask Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=context)
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=1024
    )
    
    # Step 4 — Return answer with sources
    return {
        "answer": response.choices[0].message.content,
        "sources": [
            {
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in chunks
        ]
    }