import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str = os.getenv("SUPABASE_URL", "your-supabase-url")
    supabase_key: str = os.getenv("SUPABASE_KEY", "your-supabase-key")
    jwt_secret: str = os.getenv("JWT_SECRET", "your-jwt-secret")
    
    class Config:
        env_file = ".env"

settings = Settings() 