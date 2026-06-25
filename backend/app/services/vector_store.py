import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chromadb_store")

# Use a free, local embedding model
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create our collection
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)

def store_chunks(chunks: list[str], doc_id: str, filename: str):
    """Store document chunks in ChromaDB"""
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"filename": filename, "chunk_index": i} 
                 for i in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    return len(chunks)

def search_similar_chunks(query: str, n_results: int = 3) -> list[dict]:
    """Find chunks most similar to the query"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "content": doc,
            "filename": results["metadatas"][0][i]["filename"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"]
        })
    
    return chunks