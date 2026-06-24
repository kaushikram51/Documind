from fastapi import FastAPI

app = FastAPI(
    title="DocuMind API",
    description="AI-powered knowledge assistant",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "DocuMind API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}