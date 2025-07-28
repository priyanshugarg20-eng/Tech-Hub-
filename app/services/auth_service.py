"""
Authentication service with business logic
"""

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import uuid

from app.models.user import User, UserRole, UserStatus
from app.models.tenant import Tenant
from app.core.security import SecurityUtils


class AuthService:
    """Authentication service"""
    
    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not SecurityUtils.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def create_user(db: Session, user_data: dict) -> User:
        """Create a new user"""
        # Hash password
        hashed_password = SecurityUtils.get_password_hash(user_data["password"])
        
        # Create user
        user = User(
            id=str(uuid.uuid4()),
            email=user_data["email"],
            username=user_data.get("username"),
            hashed_password=hashed_password,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data.get("phone"),
            role=user_data.get("role", UserRole.STUDENT),
            status=UserStatus.PENDING,
            tenant_id=user_data.get("tenant_id")
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    async def update_user(db: Session, user_id: str, user_data: dict) -> Optional[User]:
        """Update user information"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Update fields
        for field, value in user_data.items():
            if hasattr(user, field) and field != "id":
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    async def delete_user(db: Session, user_id: str) -> bool:
        """Delete user (soft delete)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.status = UserStatus.INACTIVE
        db.commit()
        
        return True
    
    @staticmethod
    async def verify_email(db: Session, token: str) -> bool:
        """Verify user email"""
        user = db.query(User).filter(User.email_verification_token == token).first()
        if not user:
            return False
        
        user.is_email_verified = True
        user.email_verification_token = None
        user.status = UserStatus.ACTIVE
        
        db.commit()
        
        return True
    
    @staticmethod
    async def reset_password(db: Session, token: str, new_password: str) -> bool:
        """Reset user password"""
        user = db.query(User).filter(
            User.password_reset_token == token,
            User.password_reset_expires > datetime.utcnow()
        ).first()
        
        if not user:
            return False
        
        user.hashed_password = SecurityUtils.get_password_hash(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        
        db.commit()
        
        return True
    
    @staticmethod
    async def generate_password_reset_token(db: Session, email: str) -> Optional[str]:
        """Generate password reset token"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        token = str(uuid.uuid4())
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        
        db.commit()
        
        return token
    
    @staticmethod
    async def generate_email_verification_token(db: Session, user_id: str) -> Optional[str]:
        """Generate email verification token"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        token = str(uuid.uuid4())
        user.email_verification_token = token
        
        db.commit()
        
        return token
    
    @staticmethod
    async def check_user_permissions(user: User, permission: str) -> bool:
        """Check if user has specific permission"""
        return user.has_permission(permission)
    
    @staticmethod
    async def get_user_sessions(db: Session, user_id: str) -> list:
        """Get user active sessions"""
        # This would typically query a sessions table
        # For now, return empty list
        return []
    
    @staticmethod
    async def revoke_user_session(db: Session, user_id: str, session_id: str) -> bool:
        """Revoke user session"""
        # This would typically update a sessions table
        # For now, return True
        return True
    
    @staticmethod
    async def get_user_login_history(db: Session, user_id: str, limit: int = 10) -> list:
        """Get user login history"""
        # This would typically query a login_history table
        # For now, return empty list
        return []
    
    @staticmethod
    async def update_user_preferences(db: Session, user_id: str, preferences: dict) -> bool:
        """Update user preferences"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.set_notification_preferences(preferences)
        db.commit()
        
        return True
    
    @staticmethod
    async def enable_two_factor(db: Session, user_id: str, secret: str) -> bool:
        """Enable two-factor authentication"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.two_factor_enabled = True
        user.two_factor_secret = secret
        
        db.commit()
        
        return True
    
    @staticmethod
    async def disable_two_factor(db: Session, user_id: str) -> bool:
        """Disable two-factor authentication"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        
        db.commit()
        
        return True