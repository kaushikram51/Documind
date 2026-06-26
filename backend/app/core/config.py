from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DocuMind"
    app_version: str = "0.1.0"
    groq_api_key: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()