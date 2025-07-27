"""
Configuration settings for Aiqube School Management System
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Aiqube School Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://aiqube:password@localhost:5432/aiqube_sms"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    
    # SMS (Twilio)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif",
        "application/pdf", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    # Redis (for caching and background tasks)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Geolocation
    DEFAULT_LATITUDE: float = 0.0
    DEFAULT_LONGITUDE: float = 0.0
    ATTENDANCE_RADIUS_METERS: int = 100
    
    # Subscription Plans
    BASIC_PLAN_PRICE: float = 99.0
    PROFESSIONAL_PLAN_PRICE: float = 199.0
    ENTERPRISE_PLAN_PRICE: float = 399.0
    
    # Notification Settings
    EMAIL_NOTIFICATIONS: bool = True
    SMS_NOTIFICATIONS: bool = True
    PUSH_NOTIFICATIONS: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/aiqube_sms.log"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # Multi-tenant
    TENANT_HEADER: str = "X-Tenant-ID"
    DEFAULT_TENANT: str = "default"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)