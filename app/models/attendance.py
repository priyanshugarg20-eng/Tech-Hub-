"""
Attendance system models with geolocation, QR codes, and manual tracking
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey, Float, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
import uuid


class AttendanceStatus(str, enum.Enum):
    """Attendance status types"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    LEAVE = "leave"
    HOLIDAY = "holiday"


class AttendanceMethod(str, enum.Enum):
    """Attendance method types"""
    MANUAL = "manual"
    QR_CODE = "qr_code"
    GEOLOCATION = "geolocation"
    BIOMETRIC = "biometric"
    RFID = "rfid"


class AttendanceRecord(Base):
    """Attendance record model"""
    
    __tablename__ = "attendance_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=True, index=True)
    teacher_id = Column(String(36), ForeignKey("teachers.id"), nullable=True, index=True)
    class_id = Column(String(36), ForeignKey("classes.id"), nullable=True, index=True)
    
    # Attendance Information
    date = Column(Date, nullable=False, index=True)
    time_in = Column(DateTime(timezone=True), nullable=True)
    time_out = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.ABSENT)
    method = Column(Enum(AttendanceMethod), nullable=False, default=AttendanceMethod.MANUAL)
    
    # Geolocation Information
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_address = Column(String(500), nullable=True)
    location_accuracy = Column(Float, nullable=True)  # GPS accuracy in meters
    
    # QR Code Information
    qr_code_id = Column(String(100), nullable=True)
    qr_scan_time = Column(DateTime(timezone=True), nullable=True)
    
    # Manual Attendance
    marked_by = Column(String(36), ForeignKey("users.id"), nullable=True)  # Who marked the attendance
    remarks = Column(Text, nullable=True)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verified_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    verification_time = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="attendance_records")
    user = relationship("User", back_populates="attendance_records", foreign_keys=[user_id])
    student = relationship("Student", back_populates="attendance_records")
    teacher = relationship("Teacher", back_populates="attendance_records")
    class_obj = relationship("Class", back_populates="attendance_records")
    marked_by_user = relationship("User", foreign_keys=[marked_by])
    verified_by_user = relationship("User", foreign_keys=[verified_by])
    
    def __repr__(self):
        return f"<AttendanceRecord(id={self.id}, user_id='{self.user_id}', date='{self.date}', status='{self.status}')>"
    
    @property
    def duration_minutes(self) -> int:
        """Calculate duration in minutes"""
        if self.time_in and self.time_out:
            duration = self.time_out - self.time_in
            return int(duration.total_seconds() / 60)
        return 0
    
    @property
    def is_late(self) -> bool:
        """Check if attendance is late"""
        if not self.time_in:
            return False
        
        # Define late threshold (e.g., 15 minutes after class start)
        from datetime import datetime, time
        class_start_time = time(8, 0)  # 8:00 AM
        attendance_time = self.time_in.time()
        
        return attendance_time > class_start_time
    
    def mark_present(self, method: AttendanceMethod = AttendanceMethod.MANUAL, **kwargs):
        """Mark attendance as present"""
        from datetime import datetime
        self.status = AttendanceStatus.PRESENT
        self.method = method
        self.time_in = datetime.utcnow()
        
        # Set additional fields based on method
        if method == AttendanceMethod.GEOLOCATION:
            self.latitude = kwargs.get('latitude')
            self.longitude = kwargs.get('longitude')
            self.location_address = kwargs.get('location_address')
            self.location_accuracy = kwargs.get('location_accuracy')
        elif method == AttendanceMethod.QR_CODE:
            self.qr_code_id = kwargs.get('qr_code_id')
            self.qr_scan_time = datetime.utcnow()
        elif method == AttendanceMethod.MANUAL:
            self.marked_by = kwargs.get('marked_by')
            self.remarks = kwargs.get('remarks')
    
    def mark_absent(self, reason: str = None):
        """Mark attendance as absent"""
        self.status = AttendanceStatus.ABSENT
        self.remarks = reason
    
    def mark_late(self, reason: str = None):
        """Mark attendance as late"""
        self.status = AttendanceStatus.LATE
        self.remarks = reason
    
    def mark_leave(self, reason: str = None):
        """Mark attendance as leave"""
        self.status = AttendanceStatus.LEAVE
        self.remarks = reason
    
    def verify_attendance(self, verified_by: str):
        """Verify attendance record"""
        from datetime import datetime
        self.is_verified = True
        self.verified_by = verified_by
        self.verification_time = datetime.utcnow()


class QRCode(Base):
    """QR Code model for attendance"""
    
    __tablename__ = "qr_codes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    class_id = Column(String(36), ForeignKey("classes.id"), nullable=True, index=True)
    
    # QR Code Information
    qr_code_id = Column(String(100), unique=True, nullable=False, index=True)
    qr_code_data = Column(Text, nullable=False)  # Encoded data
    qr_code_image_url = Column(String(500), nullable=True)
    
    # Validity
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    
    # Usage
    max_uses = Column(Integer, nullable=True)  # None for unlimited
    current_uses = Column(Integer, default=0)
    
    # Location
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    radius_meters = Column(Integer, default=100)  # Valid radius for scanning
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant")
    class_obj = relationship("Class")
    
    def __repr__(self):
        return f"<QRCode(id={self.id}, qr_code_id='{self.qr_code_id}', class_id='{self.class_id}')>"
    
    @property
    def is_valid(self) -> bool:
        """Check if QR code is valid"""
        from datetime import datetime
        now = datetime.utcnow()
        
        if not self.is_active:
            return False
        
        if now < self.valid_from or now > self.valid_until:
            return False
        
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        
        return True
    
    def can_be_used(self) -> bool:
        """Check if QR code can be used"""
        return self.is_valid
    
    def increment_usage(self):
        """Increment usage count"""
        self.current_uses += 1


class AttendanceSchedule(Base):
    """Attendance schedule model"""
    
    __tablename__ = "attendance_schedules"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    class_id = Column(String(36), ForeignKey("classes.id"), nullable=True, index=True)
    
    # Schedule Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Time Settings
    start_time = Column(String(10), nullable=False)  # HH:MM format
    end_time = Column(String(10), nullable=False)  # HH:MM format
    late_threshold_minutes = Column(Integer, default=15)
    
    # Days of Week (JSON string)
    days_of_week = Column(Text, nullable=False)  # [1,2,3,4,5] for Monday to Friday
    
    # Validity
    is_active = Column(Boolean, default=True)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant")
    class_obj = relationship("Class")
    
    def __repr__(self):
        return f"<AttendanceSchedule(id={self.id}, name='{self.name}', class_id='{self.class_id}')>"
    
    def get_days_of_week(self) -> list:
        """Get days of week as list"""
        import json
        if self.days_of_week:
            try:
                return json.loads(self.days_of_week)
            except json.JSONDecodeError:
                pass
        return []
    
    def set_days_of_week(self, days: list):
        """Set days of week"""
        import json
        self.days_of_week = json.dumps(days)
    
    def is_schedule_day(self, date) -> bool:
        """Check if date is a schedule day"""
        days = self.get_days_of_week()
        return date.weekday() + 1 in days  # Monday = 1, Sunday = 7
    
    def is_within_schedule_time(self, time) -> bool:
        """Check if time is within schedule"""
        from datetime import datetime, time as dt_time
        
        start_time = datetime.strptime(self.start_time, "%H:%M").time()
        end_time = datetime.strptime(self.end_time, "%H:%M").time()
        
        return start_time <= time <= end_time