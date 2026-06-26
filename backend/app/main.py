from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router

app = FastAPI(
    title=f"{settings.app_name} API",
    description="AI-powered knowledge assistant",
    version=settings.app_version
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."}
    )

app.include_router(documents_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": f"{settings.app_name} API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.app_version}