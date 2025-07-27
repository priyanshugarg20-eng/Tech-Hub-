"""
Teacher model with comprehensive teacher information
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey, Float, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
import uuid


class TeacherStatus(str, enum.Enum):
    """Teacher status types"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    RETIRED = "retired"


class TeacherQualification(str, enum.Enum):
    """Teacher qualification types"""
    BACHELORS = "bachelors"
    MASTERS = "masters"
    PHD = "phd"
    DIPLOMA = "diploma"
    CERTIFICATION = "certification"
    OTHER = "other"


class Teacher(Base):
    """Teacher model with comprehensive information"""
    
    __tablename__ = "teachers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Teacher Information
    teacher_id = Column(String(50), unique=True, nullable=False, index=True)  # School-specific ID
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    joining_date = Column(Date, nullable=False)
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)  # Senior Teacher, Head of Department, etc.
    
    # Academic Information
    qualification = Column(Enum(TeacherQualification), nullable=True)
    specialization = Column(String(255), nullable=True)  # Mathematics, Science, English, etc.
    experience_years = Column(Integer, default=0)
    status = Column(Enum(TeacherStatus), default=TeacherStatus.ACTIVE)
    
    # Personal Information
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    blood_group = Column(String(10), nullable=True)
    nationality = Column(String(50), nullable=True)
    
    # Contact Information
    emergency_contact = Column(String(50), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)
    
    # Address
    permanent_address = Column(Text, nullable=True)
    current_address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Employment Details
    employment_type = Column(String(50), nullable=True)  # Full-time, Part-time, Contract
    salary = Column(Float, nullable=True)
    bank_name = Column(String(100), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    
    # Academic Details
    previous_institution = Column(String(255), nullable=True)
    previous_designation = Column(String(100), nullable=True)
    experience_details = Column(Text, nullable=True)  # JSON string of experience
    
    # Medical Information
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    emergency_medical_info = Column(Text, nullable=True)
    
    # Transport Information
    uses_transport = Column(Boolean, default=False)
    transport_route = Column(String(100), nullable=True)
    pickup_location = Column(String(255), nullable=True)
    drop_location = Column(String(255), nullable=True)
    
    # Hostel Information
    uses_hostel = Column(Boolean, default=False)
    hostel_room = Column(String(50), nullable=True)
    hostel_block = Column(String(50), nullable=True)
    
    # Performance Metrics
    performance_rating = Column(Float, default=0.0)
    attendance_percentage = Column(Float, default=0.0)
    student_satisfaction = Column(Float, default=0.0)
    
    # Documents
    profile_picture = Column(String(500), nullable=True)
    resume = Column(String(500), nullable=True)
    certificates = Column(Text, nullable=True)  # JSON string of certificate URLs
    medical_certificate = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    tenant = relationship("Tenant", back_populates="teachers")
    classes = relationship("Class", back_populates="teacher")
    subjects = relationship("Subject", secondary="teacher_subjects", back_populates="teachers")
    attendance_records = relationship("AttendanceRecord", back_populates="teacher")
    assignments = relationship("Assignment", back_populates="teacher")
    grades = relationship("Grade", back_populates="teacher")
    hostel_record = relationship("HostelRecord", back_populates="teacher", uselist=False)
    transport_record = relationship("TransportRecord", back_populates="teacher", uselist=False)
    
    def __repr__(self):
        return f"<Teacher(id={self.id}, teacher_id='{self.teacher_id}', name='{self.user.full_name if self.user else 'Unknown'}')>"
    
    @property
    def full_name(self) -> str:
        """Get teacher's full name"""
        return self.user.full_name if self.user else "Unknown"
    
    @property
    def age(self) -> int:
        """Calculate teacher's age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def is_active(self) -> bool:
        """Check if teacher is active"""
        return self.status == TeacherStatus.ACTIVE
    
    @property
    def qualification_display(self) -> str:
        """Get display name for qualification"""
        qualification_names = {
            TeacherQualification.BACHELORS: "Bachelor's Degree",
            TeacherQualification.MASTERS: "Master's Degree",
            TeacherQualification.PHD: "Ph.D.",
            TeacherQualification.DIPLOMA: "Diploma",
            TeacherQualification.CERTIFICATION: "Certification",
            TeacherQualification.OTHER: "Other"
        }
        return qualification_names.get(self.qualification, str(self.qualification))
    
    def get_performance_metrics(self) -> dict:
        """Get teacher's performance metrics"""
        return {
            "performance_rating": self.performance_rating,
            "attendance_percentage": self.attendance_percentage,
            "student_satisfaction": self.student_satisfaction,
            "experience_years": self.experience_years,
            "specialization": self.specialization
        }
    
    def update_attendance_percentage(self, total_days: int, present_days: int):
        """Update attendance percentage"""
        if total_days > 0:
            self.attendance_percentage = (present_days / total_days) * 100
        else:
            self.attendance_percentage = 0.0
    
    def get_emergency_contacts(self) -> list:
        """Get list of emergency contacts"""
        contacts = []
        if self.emergency_contact and self.emergency_contact_phone:
            contacts.append({
                "name": self.emergency_contact,
                "relation": self.emergency_contact_relation,
                "phone": self.emergency_contact_phone
            })
        
        # Add user contact
        if self.user and self.user.phone:
            contacts.append({
                "name": self.user.full_name,
                "relation": "Self",
                "phone": self.user.phone
            })
        
        return contacts
    
    def get_experience_details(self) -> list:
        """Get teacher's experience details"""
        import json
        if self.experience_details:
            try:
                return json.loads(self.experience_details)
            except json.JSONDecodeError:
                pass
        return []
    
    def set_experience_details(self, experience_list: list):
        """Set teacher's experience details"""
        import json
        self.experience_details = json.dumps(experience_list)
    
    def get_certificates(self) -> list:
        """Get teacher's certificates"""
        import json
        if self.certificates:
            try:
                return json.loads(self.certificates)
            except json.JSONDecodeError:
                pass
        return []
    
    def set_certificates(self, certificate_list: list):
        """Set teacher's certificates"""
        import json
        self.certificates = json.dumps(certificate_list)


# Association table for teacher-subject relationship
class TeacherSubject(Base):
    """Association table for teacher-subject relationship"""
    
    __tablename__ = "teacher_subjects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String(36), ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(String(36), ForeignKey("subjects.id"), nullable=False)
    academic_year = Column(String(20), nullable=False)
    is_primary = Column(Boolean, default=False)  # Primary subject teacher
    created_at = Column(DateTime(timezone=True), server_default=func.now())