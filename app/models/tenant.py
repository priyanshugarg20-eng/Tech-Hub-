"""
Tenant model for multi-tenant architecture
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class SubscriptionPlan(str, enum.Enum):
    """Subscription plan types"""
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class TenantStatus(str, enum.Enum):
    """Tenant status types"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    TRIAL = "trial"


class Tenant(Base):
    """Tenant model for multi-tenant architecture"""
    
    __tablename__ = "tenants"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    domain = Column(String(255), unique=True, nullable=True)
    
    # Contact Information
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # School Information
    school_name = Column(String(255), nullable=False)
    school_type = Column(String(100), nullable=True)  # Primary, Secondary, University, etc.
    established_year = Column(Integer, nullable=True)
    total_students = Column(Integer, default=0)
    total_teachers = Column(Integer, default=0)
    
    # Subscription Information
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.BASIC)
    subscription_status = Column(Enum(TenantStatus), default=TenantStatus.TRIAL)
    subscription_start_date = Column(DateTime(timezone=True), server_default=func.now())
    subscription_end_date = Column(DateTime(timezone=True), nullable=True)
    trial_end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Billing Information
    monthly_fee = Column(Float, default=0.0)
    annual_fee = Column(Float, default=0.0)
    payment_method = Column(String(100), nullable=True)
    billing_email = Column(String(255), nullable=True)
    
    # Configuration
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    currency = Column(String(3), default="USD")
    
    # Features and Limits
    max_students = Column(Integer, default=100)
    max_teachers = Column(Integer, default=20)
    max_storage_gb = Column(Integer, default=10)
    features_enabled = Column(Text, nullable=True)  # JSON string of enabled features
    
    # Branding
    logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(7), default="#3B82F6")  # Hex color
    secondary_color = Column(String(7), default="#1F2937")  # Hex color
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="tenant")
    students = relationship("Student", back_populates="tenant")
    teachers = relationship("Teacher", back_populates="tenant")
    classes = relationship("Class", back_populates="tenant")
    attendance_records = relationship("AttendanceRecord", back_populates="tenant")
    fee_records = relationship("FeeRecord", back_populates="tenant")
    hostel_records = relationship("HostelRecord", back_populates="tenant")
    transport_records = relationship("TransportRecord", back_populates="tenant")
    courses = relationship("Course", back_populates="tenant")
    notifications = relationship("Notification", back_populates="tenant")
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', school='{self.school_name}')>"
    
    @property
    def is_trial_expired(self) -> bool:
        """Check if trial period has expired"""
        if not self.trial_end_date:
            return False
        from datetime import datetime
        return datetime.utcnow() > self.trial_end_date
    
    @property
    def is_subscription_expired(self) -> bool:
        """Check if subscription has expired"""
        if not self.subscription_end_date:
            return False
        from datetime import datetime
        return datetime.utcnow() > self.subscription_end_date
    
    @property
    def can_access_system(self) -> bool:
        """Check if tenant can access the system"""
        if not self.is_active:
            return False
        
        if self.subscription_status == TenantStatus.CANCELLED:
            return False
        
        if self.subscription_status == TenantStatus.TRIAL:
            return not self.is_trial_expired
        
        if self.subscription_status == TenantStatus.ACTIVE:
            return not self.is_subscription_expired
        
        return False
    
    def get_feature_limit(self, feature_name: str) -> int:
        """Get limit for a specific feature based on subscription plan"""
        limits = {
            SubscriptionPlan.BASIC: {
                "students": 100,
                "teachers": 20,
                "storage_gb": 10,
                "api_calls_per_day": 1000,
                "notifications_per_month": 1000
            },
            SubscriptionPlan.PROFESSIONAL: {
                "students": 500,
                "teachers": 50,
                "storage_gb": 50,
                "api_calls_per_day": 5000,
                "notifications_per_month": 5000
            },
            SubscriptionPlan.ENTERPRISE: {
                "students": -1,  # Unlimited
                "teachers": -1,  # Unlimited
                "storage_gb": 500,
                "api_calls_per_day": 50000,
                "notifications_per_month": 50000
            }
        }
        
        return limits.get(self.subscription_plan, {}).get(feature_name, 0)
    
    def can_use_feature(self, feature_name: str, current_usage: int = 0) -> bool:
        """Check if tenant can use a specific feature"""
        limit = self.get_feature_limit(feature_name)
        if limit == -1:  # Unlimited
            return True
        return current_usage < limit