from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=f"{settings.app_name} API",
    description="AI-powered knowledge assistant",
    version=settings.app_version
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware — allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."}
    )

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": f"{settings.app_name} API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.app_version}