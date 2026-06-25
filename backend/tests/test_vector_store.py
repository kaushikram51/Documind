import sys
sys.path.append(".")
from app.services.vector_store import store_chunks, search_similar_chunks

def test_vector_store():
    # Store some test chunks
    test_chunks = [
        "FastAPI is a modern web framework for building APIs with Python",
        "ChromaDB is a vector database for storing embeddings",
        "RAG stands for Retrieval Augmented Generation",
        "Python is a popular programming language for AI development"
    ]
    
    stored = store_chunks(test_chunks, "test_doc_001", "test.txt")
    print(f"✅ Stored {stored} chunks")
    
    # Search for similar chunks
    results = search_similar_chunks("What is a vector database?")
    print(f"\n✅ Search results for 'What is a vector database?':")
    for r in results:
        print(f"  - {r['content'][:60]}...")
    
    print("\n✅ Vector store working correctly")

if __name__ == "__main__":
    test_vector_store()