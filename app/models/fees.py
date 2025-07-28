"""
Fee management system models with comprehensive payment tracking
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey, Float, Enum, Date, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
import uuid


class FeeType(str, enum.Enum):
    """Fee type categories"""
    TUITION = "tuition"
    TRANSPORT = "transport"
    HOSTEL = "hostel"
    LIBRARY = "library"
    LABORATORY = "laboratory"
    SPORTS = "sports"
    EXAMINATION = "examination"
    MISCELLANEOUS = "miscellaneous"
    UNIFORM = "uniform"
    BOOKS = "books"
    MEALS = "meals"
    ACTIVITIES = "activities"


class PaymentStatus(str, enum.Enum):
    """Payment status types"""
    PENDING = "pending"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    """Payment method types"""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    ONLINE_PAYMENT = "online_payment"
    MOBILE_PAYMENT = "mobile_payment"
    SCHOLARSHIP = "scholarship"
    WAIVER = "waiver"


class FeeRecord(Base):
    """Fee record model"""
    
    __tablename__ = "fee_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    
    # Fee Information
    fee_type = Column(Enum(FeeType), nullable=False)
    academic_year = Column(String(20), nullable=False)  # 2023-2024
    semester = Column(String(20), nullable=True)  # Fall, Spring, Summer
    month = Column(String(20), nullable=True)  # For monthly fees
    
    # Amount Information
    total_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), default=0.0)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    late_fee = Column(Numeric(10, 2), default=0.0)
    
    # Due Dates
    due_date = Column(Date, nullable=False)
    grace_period_days = Column(Integer, default=5)
    
    # Status
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    is_waived = Column(Boolean, default=False)
    waiver_reason = Column(Text, nullable=True)
    
    # Description
    description = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="fee_records")
    student = relationship("Student", back_populates="fee_records")
    payments = relationship("Payment", back_populates="fee_record")
    
    def __repr__(self):
        return f"<FeeRecord(id={self.id}, student_id='{self.student_id}', fee_type='{self.fee_type}', amount='{self.total_amount}')>"
    
    @property
    def remaining_amount(self) -> float:
        """Calculate remaining amount"""
        return float(self.total_amount - self.paid_amount - self.discount_amount)
    
    @property
    def is_overdue(self) -> bool:
        """Check if fee is overdue"""
        from datetime import date, timedelta
        today = date.today()
        grace_date = self.due_date + timedelta(days=self.grace_period_days)
        return today > grace_date and self.remaining_amount > 0
    
    @property
    def days_overdue(self) -> int:
        """Calculate days overdue"""
        if not self.is_overdue:
            return 0
        from datetime import date, timedelta
        today = date.today()
        grace_date = self.due_date + timedelta(days=self.grace_period_days)
        return (today - grace_date).days
    
    def calculate_late_fee(self) -> float:
        """Calculate late fee based on overdue days"""
        if not self.is_overdue:
            return 0.0
        
        # Simple late fee calculation (can be customized)
        overdue_amount = self.remaining_amount
        late_fee_rate = 0.05  # 5% per month
        months_overdue = self.days_overdue / 30
        
        return float(overdue_amount * late_fee_rate * months_overdue)
    
    def update_payment_status(self):
        """Update payment status based on amounts"""
        if self.is_waived:
            self.status = PaymentStatus.PAID
        elif self.remaining_amount <= 0:
            self.status = PaymentStatus.PAID
        elif self.paid_amount > 0:
            self.status = PaymentStatus.PARTIAL
        elif self.is_overdue:
            self.status = PaymentStatus.OVERDUE
        else:
            self.status = PaymentStatus.PENDING


class Payment(Base):
    """Payment record model"""
    
    __tablename__ = "payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    fee_record_id = Column(String(36), ForeignKey("fee_records.id"), nullable=False, index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Payment Information
    payment_id = Column(String(50), unique=True, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    
    # Payment Details
    transaction_id = Column(String(100), nullable=True)
    reference_number = Column(String(100), nullable=True)
    bank_name = Column(String(100), nullable=True)
    cheque_number = Column(String(50), nullable=True)
    
    # Status
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    verification_time = Column(DateTime(timezone=True), nullable=True)
    
    # Additional Information
    remarks = Column(Text, nullable=True)
    receipt_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    fee_record = relationship("FeeRecord", back_populates="payments")
    tenant = relationship("Tenant")
    verified_by_user = relationship("User")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, payment_id='{self.payment_id}', amount='{self.amount}', method='{self.payment_method}')>"
    
    def verify_payment(self, verified_by: str):
        """Verify payment"""
        from datetime import datetime
        self.is_verified = True
        self.verified_by = verified_by
        self.verification_time = datetime.utcnow()
        self.status = PaymentStatus.PAID


class FeeStructure(Base):
    """Fee structure model"""
    
    __tablename__ = "fee_structures"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Structure Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    academic_year = Column(String(20), nullable=False)
    grade = Column(String(50), nullable=True)  # For grade-specific fees
    
    # Fee Components (JSON string)
    fee_components = Column(Text, nullable=False)  # JSON array of fee components
    
    # Validity
    is_active = Column(Boolean, default=True)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant")
    
    def __repr__(self):
        return f"<FeeStructure(id={self.id}, name='{self.name}', academic_year='{self.academic_year}')>"
    
    def get_fee_components(self) -> list:
        """Get fee components as list"""
        import json
        if self.fee_components:
            try:
                return json.loads(self.fee_components)
            except json.JSONDecodeError:
                pass
        return []
    
    def set_fee_components(self, components: list):
        """Set fee components"""
        import json
        self.fee_components = json.dumps(components)
    
    def calculate_total_fee(self) -> float:
        """Calculate total fee from components"""
        components = self.get_fee_components()
        total = 0.0
        for component in components:
            total += component.get('amount', 0)
        return total


class FeeDiscount(Base):
    """Fee discount model"""
    
    __tablename__ = "fee_discounts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=True, index=True)
    
    # Discount Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(String(50), nullable=False)  # percentage, fixed_amount
    discount_value = Column(Numeric(10, 2), nullable=False)
    
    # Applicability
    fee_types = Column(Text, nullable=True)  # JSON array of applicable fee types
    academic_year = Column(String(20), nullable=True)
    semester = Column(String(20), nullable=True)
    
    # Validity
    is_active = Column(Boolean, default=True)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant")
    student = relationship("Student")
    
    def __repr__(self):
        return f"<FeeDiscount(id={self.id}, name='{self.name}', value='{self.discount_value}')>"
    
    def get_fee_types(self) -> list:
        """Get applicable fee types"""
        import json
        if self.fee_types:
            try:
                return json.loads(self.fee_types)
            except json.JSONDecodeError:
                pass
        return []
    
    def set_fee_types(self, fee_types: list):
        """Set applicable fee types"""
        import json
        self.fee_types = json.dumps(fee_types)
    
    def calculate_discount(self, amount: float) -> float:
        """Calculate discount amount"""
        if self.discount_type == "percentage":
            return amount * (self.discount_value / 100)
        else:
            return min(amount, float(self.discount_value))