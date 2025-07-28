"""
Authentication API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import uuid

from app.core.database import get_db
from app.core.security import SecurityUtils, get_current_user, authenticate_user
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.tenant import Tenant, TenantStatus
from app.schemas.auth import (
    LoginRequest, LoginResponse, RegisterRequest, RegisterResponse,
    PasswordResetRequest, PasswordResetConfirm, TokenRefresh,
    UserProfile, ChangePasswordRequest
)
from app.services.auth_service import AuthService
from app.services.notification_service import NotificationService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """User login endpoint"""
    try:
        # Authenticate user
        user = authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user can login
        if not user.can_login:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is locked or inactive"
            )
        
        # Check tenant access if user is not super admin
        if user.role != UserRole.SUPER_ADMIN and user.tenant_id:
            tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
            if not tenant or not tenant.can_access_system:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="School subscription has expired or is inactive"
                )
        
        # Reset failed login attempts
        user.reset_failed_login()
        user.update_last_login()
        db.commit()
        
        # Create tokens
        access_token = SecurityUtils.create_access_token(
            data={"sub": str(user.id), "role": user.role, "tenant_id": user.tenant_id}
        )
        refresh_token = SecurityUtils.create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserProfile(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
                tenant_id=user.tenant_id,
                is_email_verified=user.is_email_verified
            )
        )
    
    except HTTPException:
        # Increment failed login attempts
        user = db.query(User).filter(User.email == login_data.email).first()
        if user:
            user.increment_failed_login()
            db.commit()
        raise


@router.post("/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """User registration endpoint"""
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == register_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        if register_data.username:
            existing_username = db.query(User).filter(User.username == register_data.username).first()
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Hash password
        hashed_password = SecurityUtils.get_password_hash(register_data.password)
        
        # Create user
        user = User(
            id=str(uuid.uuid4()),
            email=register_data.email,
            username=register_data.username,
            hashed_password=hashed_password,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            phone=register_data.phone,
            role=register_data.role or UserRole.STUDENT,
            status=UserStatus.PENDING
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Send welcome email in background
        background_tasks.add_task(
            NotificationService.send_welcome_email,
            user.email,
            user.full_name
        )
        
        return RegisterResponse(
            message="Registration successful. Please check your email for verification.",
            user_id=user.id
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    try:
        # Verify refresh token
        payload = SecurityUtils.verify_token(refresh_data.refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create new tokens
        access_token = SecurityUtils.create_access_token(
            data={"sub": str(user.id), "role": user.role, "tenant_id": user.tenant_id}
        )
        refresh_token = SecurityUtils.create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserProfile(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
                tenant_id=user.tenant_id,
                is_email_verified=user.is_email_verified
            )
        )
    
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/password-reset-request")
async def password_reset_request(
    reset_data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    user = db.query(User).filter(User.email == reset_data.email).first()
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If email exists, password reset link has been sent"}
    
    # Generate reset token
    reset_token = str(uuid.uuid4())
    user.password_reset_token = reset_token
    user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
    
    db.commit()
    
    # Send password reset email in background
    background_tasks.add_task(
        NotificationService.send_password_reset_email,
        user.email,
        user.full_name,
        reset_token
    )
    
    return {"message": "If email exists, password reset link has been sent"}


@router.post("/password-reset-confirm")
async def password_reset_confirm(
    confirm_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirm password reset"""
    user = db.query(User).filter(
        User.password_reset_token == confirm_data.token,
        User.password_reset_expires > datetime.utcnow()
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Update password
    user.hashed_password = SecurityUtils.get_password_hash(confirm_data.new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    
    db.commit()
    
    return {"message": "Password reset successful"}


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    # Verify current password
    if not SecurityUtils.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.hashed_password = SecurityUtils.get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role,
        tenant_id=current_user.tenant_id,
        is_email_verified=current_user.is_email_verified
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """User logout endpoint"""
    # In a real implementation, you might want to blacklist the token
    # For now, we'll just return a success message
    return {"message": "Logout successful"}


@router.post("/verify-email/{token}")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify user email"""
    user = db.query(User).filter(User.email_verification_token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    
    user.is_email_verified = True
    user.email_verification_token = None
    user.status = UserStatus.ACTIVE
    
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/resend-verification")
async def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resend email verification"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Generate new verification token
    verification_token = str(uuid.uuid4())
    user.email_verification_token = verification_token
    
    db.commit()
    
    # Send verification email in background
    background_tasks.add_task(
        NotificationService.send_verification_email,
        user.email,
        user.full_name,
        verification_token
    )
    
    return {"message": "Verification email sent"}


@router.get("/roles")
async def get_roles():
    """Get available user roles"""
    from app.core.security import ROLES
    return {"roles": ROLES}