from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DocuMind"
    app_version: str = "0.1.0"
    groq_api_key: str = ""
    
    # Auth settings
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = ""

    class Config:
        env_file = ".env"

settings = Settings()