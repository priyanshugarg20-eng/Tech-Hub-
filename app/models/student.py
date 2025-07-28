"""
Student model with comprehensive student information
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, ForeignKey, Float, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
import uuid


class StudentStatus(str, enum.Enum):
    """Student status types"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"
    SUSPENDED = "suspended"


class StudentGrade(str, enum.Enum):
    """Student grade levels"""
    KINDERGARTEN = "kindergarten"
    GRADE_1 = "grade_1"
    GRADE_2 = "grade_2"
    GRADE_3 = "grade_3"
    GRADE_4 = "grade_4"
    GRADE_5 = "grade_5"
    GRADE_6 = "grade_6"
    GRADE_7 = "grade_7"
    GRADE_8 = "grade_8"
    GRADE_9 = "grade_9"
    GRADE_10 = "grade_10"
    GRADE_11 = "grade_11"
    GRADE_12 = "grade_12"
    UNIVERSITY = "university"


class Student(Base):
    """Student model with comprehensive information"""
    
    __tablename__ = "students"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Student Information
    student_id = Column(String(50), unique=True, nullable=False, index=True)  # School-specific ID
    admission_number = Column(String(50), unique=True, nullable=False, index=True)
    admission_date = Column(Date, nullable=False)
    grade = Column(Enum(StudentGrade), nullable=False)
    section = Column(String(10), nullable=True)  # A, B, C, etc.
    roll_number = Column(Integer, nullable=True)
    
    # Academic Information
    current_grade = Column(Enum(StudentGrade), nullable=False)
    current_section = Column(String(10), nullable=True)
    academic_year = Column(String(20), nullable=False)  # 2023-2024
    status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)
    
    # Personal Information
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    blood_group = Column(String(10), nullable=True)
    nationality = Column(String(50), nullable=True)
    religion = Column(String(50), nullable=True)
    mother_tongue = Column(String(50), nullable=True)
    
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
    
    # Academic Details
    previous_school = Column(String(255), nullable=True)
    previous_grade = Column(String(50), nullable=True)
    transfer_certificate = Column(String(500), nullable=True)
    
    # Medical Information
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
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
    
    # Academic Performance
    cgpa = Column(Float, default=0.0)
    total_credits = Column(Integer, default=0)
    attendance_percentage = Column(Float, default=0.0)
    
    # Documents
    profile_picture = Column(String(500), nullable=True)
    birth_certificate = Column(String(500), nullable=True)
    transfer_certificate_url = Column(String(500), nullable=True)
    medical_certificate = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    tenant = relationship("Tenant", back_populates="students")
    parents = relationship("Parent", secondary="student_parents", back_populates="children")
    classes = relationship("Class", secondary="student_classes", back_populates="students")
    attendance_records = relationship("AttendanceRecord", back_populates="student")
    fee_records = relationship("FeeRecord", back_populates="student")
    assignments = relationship("Assignment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    hostel_record = relationship("HostelRecord", back_populates="student", uselist=False)
    transport_record = relationship("TransportRecord", back_populates="student", uselist=False)
    
    def __repr__(self):
        return f"<Student(id={self.id}, student_id='{self.student_id}', name='{self.user.full_name if self.user else 'Unknown'}')>"
    
    @property
    def full_name(self) -> str:
        """Get student's full name"""
        return self.user.full_name if self.user else "Unknown"
    
    @property
    def age(self) -> int:
        """Calculate student's age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def is_active(self) -> bool:
        """Check if student is active"""
        return self.status == StudentStatus.ACTIVE
    
    @property
    def grade_display(self) -> str:
        """Get display name for grade"""
        grade_names = {
            StudentGrade.KINDERGARTEN: "Kindergarten",
            StudentGrade.GRADE_1: "Grade 1",
            StudentGrade.GRADE_2: "Grade 2",
            StudentGrade.GRADE_3: "Grade 3",
            StudentGrade.GRADE_4: "Grade 4",
            StudentGrade.GRADE_5: "Grade 5",
            StudentGrade.GRADE_6: "Grade 6",
            StudentGrade.GRADE_7: "Grade 7",
            StudentGrade.GRADE_8: "Grade 8",
            StudentGrade.GRADE_9: "Grade 9",
            StudentGrade.GRADE_10: "Grade 10",
            StudentGrade.GRADE_11: "Grade 11",
            StudentGrade.GRADE_12: "Grade 12",
            StudentGrade.UNIVERSITY: "University"
        }
        return grade_names.get(self.current_grade, str(self.current_grade))
    
    def get_academic_progress(self) -> dict:
        """Get student's academic progress"""
        return {
            "cgpa": self.cgpa,
            "total_credits": self.total_credits,
            "attendance_percentage": self.attendance_percentage,
            "current_grade": self.grade_display,
            "academic_year": self.academic_year
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
        
        # Add parent contacts
        for parent in self.parents:
            if parent.user and parent.user.phone:
                contacts.append({
                    "name": parent.user.full_name,
                    "relation": "Parent",
                    "phone": parent.user.phone
                })
        
        return contacts


# Association table for student-parent relationship
class StudentParent(Base):
    """Association table for student-parent relationship"""
    
    __tablename__ = "student_parents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    parent_id = Column(String(36), ForeignKey("parents.id"), nullable=False)
    relationship = Column(String(50), nullable=False)  # Father, Mother, Guardian
    is_primary_contact = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Association table for student-class relationship
class StudentClass(Base):
    """Association table for student-class relationship"""
    
    __tablename__ = "student_classes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    class_id = Column(String(36), ForeignKey("classes.id"), nullable=False)
    academic_year = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())