from pydantic_settings import BaseSettings
from typing import Optional, Sequence
from datetime import timedelta
from authx.types import AlgorithmType
from typing import Literal

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # JWT Configuration
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: AlgorithmType = "HS256"
    jwt_access_token_expires: timedelta = timedelta(minutes=15)  
    jwt_refresh_token_expires: timedelta = timedelta(minutes=30)
    
    # Database Configuration
    database_url: Optional[str] = None
    
    # CORS Configuration
    cors_origins: Sequence[str] = ["http://localhost:3000", "https://localhost:3001"]

    # Cookie Configuration
    cookie_secret_key: str = "your-cookie-secret-key-change-in-production"
    cookie_name: str = "refresh_token"
    cookie_max_age: int = int(jwt_refresh_token_expires.total_seconds())
    cookie_http_only: bool = True
    cookie_secure: bool = True
    cookie_samesite: Literal['lax', 'strict', 'none'] = 'strict'
    cookie_path: str = '/'
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create global settings instance
settings = Settings() 