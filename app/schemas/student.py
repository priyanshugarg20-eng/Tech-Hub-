"""
Student schemas
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import date
from app.models.student import StudentStatus, StudentGrade


class StudentCreate(BaseModel):
    """Student creation schema"""
    email: EmailStr
    username: Optional[str] = None
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    
    # Student Information
    student_id: str
    admission_number: str
    admission_date: date
    grade: StudentGrade
    academic_year: str
    
    # Personal Information
    date_of_birth: date
    gender: str
    blood_group: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    mother_tongue: Optional[str] = None
    
    # Contact Information
    emergency_contact: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    
    # Address
    permanent_address: Optional[str] = None
    current_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    
    # Academic Details
    previous_school: Optional[str] = None
    previous_grade: Optional[str] = None
    
    # Medical Information
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_medical_info: Optional[str] = None
    
    # Transport Information
    uses_transport: bool = False
    transport_route: Optional[str] = None
    pickup_location: Optional[str] = None
    drop_location: Optional[str] = None
    
    # Hostel Information
    uses_hostel: bool = False
    hostel_room: Optional[str] = None
    hostel_block: Optional[str] = None


class StudentUpdate(BaseModel):
    """Student update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    
    # Student Information
    current_grade: Optional[StudentGrade] = None
    academic_year: Optional[str] = None
    status: Optional[StudentStatus] = None
    
    # Personal Information
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    mother_tongue: Optional[str] = None
    
    # Contact Information
    emergency_contact: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    
    # Address
    permanent_address: Optional[str] = None
    current_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    
    # Medical Information
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_medical_info: Optional[str] = None
    
    # Transport Information
    uses_transport: Optional[bool] = None
    transport_route: Optional[str] = None
    pickup_location: Optional[str] = None
    drop_location: Optional[str] = None
    
    # Hostel Information
    uses_hostel: Optional[bool] = None
    hostel_room: Optional[str] = None
    hostel_block: Optional[str] = None


class StudentResponse(BaseModel):
    """Student response schema"""
    id: str
    student_id: str
    admission_number: str
    admission_date: date
    grade: StudentGrade
    current_grade: StudentGrade
    academic_year: str
    status: StudentStatus
    
    # Personal Information
    date_of_birth: date
    gender: str
    blood_group: Optional[str]
    nationality: Optional[str]
    religion: Optional[str]
    mother_tongue: Optional[str]
    
    # Contact Information
    emergency_contact: Optional[str]
    emergency_contact_relation: Optional[str]
    emergency_contact_phone: Optional[str]
    
    # Address
    permanent_address: Optional[str]
    current_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    
    # Academic Details
    previous_school: Optional[str]
    previous_grade: Optional[str]
    
    # Medical Information
    medical_conditions: Optional[str]
    allergies: Optional[str]
    medications: Optional[str]
    emergency_medical_info: Optional[str]
    
    # Transport Information
    uses_transport: bool
    transport_route: Optional[str]
    pickup_location: Optional[str]
    drop_location: Optional[str]
    
    # Hostel Information
    uses_hostel: bool
    hostel_room: Optional[str]
    hostel_block: Optional[str]
    
    # Academic Performance
    cgpa: float
    total_credits: int
    attendance_percentage: float
    
    # User Information
    user_id: str
    tenant_id: str
    
    # Timestamps
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True


class StudentList(BaseModel):
    """Student list response schema"""
    students: List[StudentResponse]
    total: int
    skip: int
    limit: int


class StudentSearch(BaseModel):
    """Student search schema"""
    search: Optional[str] = None
    grade: Optional[StudentGrade] = None
    status: Optional[StudentStatus] = None
    skip: int = 0
    limit: int = 100


class StudentStats(BaseModel):
    """Student statistics schema"""
    total_students: int
    active_students: int
    grade_distribution: dict
    attendance_average: float
    fee_collection_rate: float


class StudentAttendance(BaseModel):
    """Student attendance schema"""
    id: str
    date: date
    status: str
    time_in: Optional[str]
    time_out: Optional[str]
    method: str
    remarks: Optional[str]


class StudentGrade(BaseModel):
    """Student grade schema"""
    id: str
    subject: str
    grade: str
    score: float
    semester: str
    academic_year: str
    remarks: Optional[str]


class StudentFee(BaseModel):
    """Student fee schema"""
    id: str
    fee_type: str
    total_amount: float
    paid_amount: float
    remaining_amount: float
    due_date: date
    status: str
    description: Optional[str]