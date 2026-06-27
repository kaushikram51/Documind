import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

VECTOR_STORE_FILE = "./vector_store.json"

def _load_store() -> dict:
    if not os.path.exists(VECTOR_STORE_FILE):
        return {"documents": [], "metadatas": []}
    with open(VECTOR_STORE_FILE, "r") as f:
        return json.load(f)

def _save_store(data: dict):
    with open(VECTOR_STORE_FILE, "w") as f:
        json.dump(data, f)

def store_chunks(chunks: list[str], doc_id: str, filename: str):
    store = _load_store()
    for i, chunk in enumerate(chunks):
        store["documents"].append(chunk)
        store["metadatas"].append({
            "doc_id": doc_id,
            "filename": filename,
            "chunk_index": i
        })
    _save_store(store)
    return len(chunks)

def search_similar_chunks(query: str, n_results: int = 3) -> list[dict]:
    store = _load_store()
    documents = store["documents"]
    metadatas = store["metadatas"]

    if not documents:
        return []

    # Use TF-IDF for similarity search
    vectorizer = TfidfVectorizer()
    all_texts = documents + [query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(query_vector, doc_vectors)[0]
    top_indices = similarities.argsort()[-n_results:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "content": documents[idx],
            "filename": metadatas[idx]["filename"],
            "chunk_index": metadatas[idx]["chunk_index"]
        })

    return results