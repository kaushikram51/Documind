import chromadb
from chromadb import Settings

# Use ephemeral client - no embedding function dependency
client = chromadb.EphemeralClient()

collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

def store_chunks(chunks: list[str], doc_id: str, filename: str):
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