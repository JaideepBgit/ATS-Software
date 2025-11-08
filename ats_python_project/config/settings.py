"""
Configuration settings for the ATS Python Project
"""
import os
from typing import List
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = os.getenv("APP_NAME", "ATS Python Project")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # LM Studio Configuration
    lm_studio_base_url: str = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    lm_studio_api_key: str = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
    lm_studio_model_name: str = os.getenv("LM_STUDIO_MODEL_NAME", "")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ats_database.db")
    
    # File Processing
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    allowed_file_types: List[str] = os.getenv("ALLOWED_FILE_TYPES", "pdf,docx,txt").split(",")
    upload_directory: str = os.getenv("UPLOAD_DIRECTORY", "./data/uploads")
    
    # Scoring and Matching
    min_match_score: float = float(os.getenv("MIN_MATCH_SCORE", "0.6"))
    max_results: int = int(os.getenv("MAX_RESULTS", "50"))
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
