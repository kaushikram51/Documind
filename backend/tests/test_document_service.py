from app.services.document_service import chunk_text

def test_chunk_text():
    sample_text = " ".join(["word"] * 1200)
    chunks = chunk_text(sample_text, chunk_size=500, overlap=50)
    
    print(f"Total chunks: {len(chunks)}")
    print(f"First chunk word count: {len(chunks[0].split())}")
    print(f"Last chunk word count: {len(chunks[-1].split())}")
    
    assert len(chunks) > 1
    print("✅ All tests passed")

if __name__ == "__main__":
    test_chunk_text()