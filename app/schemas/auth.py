"""
Authentication schemas
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from app.models.user import UserRole


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    refresh_token: str
    token_type: str
    user: 'UserProfile'


class RegisterRequest(BaseModel):
    """Registration request schema"""
    email: EmailStr
    username: Optional[str] = None
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: Optional[UserRole] = UserRole.STUDENT
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class RegisterResponse(BaseModel):
    """Registration response schema"""
    message: str
    user_id: str


class TokenRefresh(BaseModel):
    """Token refresh request schema"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserProfile(BaseModel):
    """User profile schema"""
    id: str
    email: str
    username: Optional[str]
    first_name: str
    last_name: str
    role: UserRole
    tenant_id: Optional[str]
    is_email_verified: bool
    
    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """User update request schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None


class NotificationPreferences(BaseModel):
    """Notification preferences schema"""
    email: bool = True
    sms: bool = False
    push: bool = True
    attendance_alerts: bool = True
    fee_reminders: bool = True
    grade_updates: bool = True
    assignment_deadlines: bool = True


class TwoFactorSetup(BaseModel):
    """Two-factor authentication setup schema"""
    enable: bool
    secret: Optional[str] = None
    backup_codes: Optional[list] = None


class TwoFactorVerify(BaseModel):
    """Two-factor authentication verification schema"""
    code: str


class SessionInfo(BaseModel):
    """Session information schema"""
    user_id: str
    role: UserRole
    tenant_id: Optional[str]
    login_time: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class LoginHistory(BaseModel):
    """Login history schema"""
    id: str
    login_time: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    success: bool
    failure_reason: Optional[str] = None
    
    class Config:
        from_attributes = True