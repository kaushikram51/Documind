from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=f"{settings.app_name} API",
    description="AI-powered knowledge assistant",
    version=settings.app_version
)

@app.get("/")
def root():
    return {"message": f"{settings.app_name} API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.app_version}