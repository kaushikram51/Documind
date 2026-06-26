from fastapi import FastAPI
from app.core.config import settings
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router

app = FastAPI(
    title=f"{settings.app_name} API",
    description="AI-powered knowledge assistant",
    version=settings.app_version
)

app.include_router(documents_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": f"{settings.app_name} API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.app_version}