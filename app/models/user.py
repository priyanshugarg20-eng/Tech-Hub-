"""
User model with role-based access control
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
import uuid


class UserRole(str, enum.Enum):
    """User role types"""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"
    STAFF = "staff"


class UserStatus(str, enum.Enum):
    """User status types"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User(Base):
    """User model with role-based access control"""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    date_of_birth = Column(DateTime(timezone=True), nullable=True)
    gender = Column(String(20), nullable=True)
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Profile
    profile_picture = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Role and Status
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    
    # Multi-tenant
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=True, index=True)
    
    # Authentication
    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Preferences
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    notification_preferences = Column(Text, nullable=True)  # JSON string
    
    # Security
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime(timezone=True), nullable=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    parent_profile = relationship("Parent", back_populates="user", uselist=False)
    
    # Notifications
    notifications = relationship("Notification", back_populates="user")
    
    # Attendance records (for students/teachers)
    attendance_records = relationship("AttendanceRecord", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def display_name(self) -> str:
        """Get user's display name (username or full name)"""
        return self.username or self.full_name
    
    @property
    def is_active(self) -> bool:
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is locked"""
        if not self.account_locked_until:
            return False
        from datetime import datetime
        return datetime.utcnow() < self.account_locked_until
    
    @property
    def can_login(self) -> bool:
        """Check if user can login"""
        return self.is_active and not self.is_locked
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        permissions = {
            UserRole.SUPER_ADMIN: [
                "manage_platform", "manage_tenants", "manage_subscriptions",
                "view_all_data", "manage_users", "manage_system"
            ],
            UserRole.ADMIN: [
                "manage_school", "manage_students", "manage_teachers",
                "manage_staff", "view_reports", "manage_fees",
                "manage_hostel", "manage_transport"
            ],
            UserRole.TEACHER: [
                "manage_classes", "manage_students", "take_attendance",
                "grade_assignments", "view_student_progress",
                "create_assignments", "send_notifications"
            ],
            UserRole.STUDENT: [
                "view_own_data", "submit_assignments", "view_grades",
                "view_schedule", "view_attendance"
            ],
            UserRole.PARENT: [
                "view_child_data", "view_child_grades", "view_child_attendance",
                "pay_fees", "receive_notifications"
            ],
            UserRole.STAFF: [
                "manage_attendance", "manage_fees", "view_reports",
                "send_notifications"
            ]
        }
        
        user_permissions = permissions.get(self.role, [])
        return permission in user_permissions
    
    def can_access_tenant(self, tenant_id: str) -> bool:
        """Check if user can access a specific tenant"""
        if self.role == UserRole.SUPER_ADMIN:
            return True
        return self.tenant_id == tenant_id
    
    def increment_failed_login(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            from datetime import datetime, timedelta
            self.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
    
    def reset_failed_login(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
    
    def update_last_login(self):
        """Update last login timestamp"""
        from datetime import datetime
        self.last_login = datetime.utcnow()
    
    def get_notification_preferences(self) -> dict:
        """Get user's notification preferences"""
        import json
        if self.notification_preferences:
            try:
                return json.loads(self.notification_preferences)
            except json.JSONDecodeError:
                pass
        return {
            "email": True,
            "sms": False,
            "push": True,
            "attendance_alerts": True,
            "fee_reminders": True,
            "grade_updates": True,
            "assignment_deadlines": True
        }
    
    def set_notification_preferences(self, preferences: dict):
        """Set user's notification preferences"""
        import json
        self.notification_preferences = json.dumps(preferences)