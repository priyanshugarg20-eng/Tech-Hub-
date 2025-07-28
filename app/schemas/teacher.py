from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, validator, Field
from enum import Enum

from app.models.teacher import TeacherStatus, TeacherQualification
from app.schemas.auth import UserUpdateRequest


class TeacherQualificationEnum(str, Enum):
    """Teacher qualification options"""
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"
    DIPLOMA = "diploma"
    CERTIFICATION = "certification"
    OTHER = "other"


class TeacherStatusEnum(str, Enum):
    """Teacher status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"


class TeacherCreate(BaseModel):
    """Schema for creating a new teacher"""
    # User account details
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    
    # Teacher-specific details
    employee_id: str = Field(..., min_length=1, max_length=20)
    date_of_birth: date
    gender: str = Field(..., regex="^(male|female|other)$")
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5, max_length=200)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    country: str = Field(..., min_length=2, max_length=50)
    postal_code: str = Field(..., min_length=3, max_length=10)
    
    # Academic details
    qualification: TeacherQualificationEnum
    specialization: str = Field(..., min_length=2, max_length=100)
    hire_date: date
    salary: Optional[float] = Field(None, ge=0)
    
    # Emergency contact
    emergency_contact_name: str = Field(..., min_length=2, max_length=100)
    emergency_contact_phone: str = Field(..., min_length=10, max_length=15)
    emergency_contact_relationship: str = Field(..., min_length=2, max_length=50)
    
    # Medical information
    medical_conditions: Optional[str] = Field(None, max_length=500)
    allergies: Optional[str] = Field(None, max_length=500)
    blood_group: Optional[str] = Field(None, regex="^(A|B|AB|O)[+-]$")
    
    # Transport and hostel
    transport_required: bool = False
    transport_route: Optional[str] = Field(None, max_length=100)
    hostel_required: bool = False
    hostel_room: Optional[str] = Field(None, max_length=20)
    
    # Experience and certificates
    experience_years: Optional[int] = Field(None, ge=0)
    experience_details: Optional[Dict[str, Any]] = None
    certificates: Optional[Dict[str, Any]] = None
    
    # Additional information
    bio: Optional[str] = Field(None, max_length=1000)
    profile_picture: Optional[str] = None
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v
    
    @validator('hire_date')
    def validate_hire_date(cls, v):
        if v > date.today():
            raise ValueError('Hire date cannot be in the future')
        return v
    
    @validator('phone', 'emergency_contact_phone')
    def validate_phone(cls, v):
        if not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone number must contain only digits, spaces, hyphens, and plus sign')
        return v


class TeacherUpdate(BaseModel):
    """Schema for updating teacher information"""
    # Personal information
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, regex="^(male|female|other)$")
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    
    # Address information
    address: Optional[str] = Field(None, min_length=5, max_length=200)
    city: Optional[str] = Field(None, min_length=2, max_length=50)
    state: Optional[str] = Field(None, min_length=2, max_length=50)
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=3, max_length=10)
    
    # Academic details
    qualification: Optional[TeacherQualificationEnum] = None
    specialization: Optional[str] = Field(None, min_length=2, max_length=100)
    hire_date: Optional[date] = None
    salary: Optional[float] = Field(None, ge=0)
    status: Optional[TeacherStatusEnum] = None
    
    # Emergency contact
    emergency_contact_name: Optional[str] = Field(None, min_length=2, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, min_length=10, max_length=15)
    emergency_contact_relationship: Optional[str] = Field(None, min_length=2, max_length=50)
    
    # Medical information
    medical_conditions: Optional[str] = Field(None, max_length=500)
    allergies: Optional[str] = Field(None, max_length=500)
    blood_group: Optional[str] = Field(None, regex="^(A|B|AB|O)[+-]$")
    
    # Transport and hostel
    transport_required: Optional[bool] = None
    transport_route: Optional[str] = Field(None, max_length=100)
    hostel_required: Optional[bool] = None
    hostel_room: Optional[str] = Field(None, max_length=20)
    
    # Experience and certificates
    experience_years: Optional[int] = Field(None, ge=0)
    experience_details: Optional[Dict[str, Any]] = None
    certificates: Optional[Dict[str, Any]] = None
    
    # Additional information
    bio: Optional[str] = Field(None, max_length=1000)
    profile_picture: Optional[str] = None
    
    # User account updates
    user_update: Optional[UserUpdateRequest] = None
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v and v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v
    
    @validator('hire_date')
    def validate_hire_date(cls, v):
        if v and v > date.today():
            raise ValueError('Hire date cannot be in the future')
        return v
    
    @validator('phone', 'emergency_contact_phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone number must contain only digits, spaces, hyphens, and plus sign')
        return v


class TeacherResponse(BaseModel):
    """Schema for teacher response data"""
    id: int
    user_id: int
    tenant_id: int
    employee_id: str
    date_of_birth: date
    gender: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    qualification: TeacherQualificationEnum
    specialization: str
    hire_date: date
    salary: Optional[float]
    status: TeacherStatusEnum
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relationship: str
    medical_conditions: Optional[str]
    allergies: Optional[str]
    blood_group: Optional[str]
    transport_required: bool
    transport_route: Optional[str]
    hostel_required: bool
    hostel_room: Optional[str]
    experience_years: Optional[int]
    experience_details: Optional[Dict[str, Any]]
    certificates: Optional[Dict[str, Any]]
    bio: Optional[str]
    profile_picture: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Derived properties
    full_name: str
    age: int
    is_active: bool
    qualification_display: str
    emergency_contacts: Dict[str, Any]
    
    # User information
    user_email: str
    user_username: str
    user_first_name: str
    user_last_name: str
    user_status: str
    
    class Config:
        from_attributes = True


class TeacherList(BaseModel):
    """Schema for paginated teacher list"""
    teachers: List[TeacherResponse]
    total: int
    skip: int
    limit: int


class TeacherSearch(BaseModel):
    """Schema for teacher search parameters"""
    name: Optional[str] = None
    status: Optional[TeacherStatusEnum] = None
    qualification: Optional[TeacherQualificationEnum] = None
    specialization: Optional[str] = None
    employee_id: Optional[str] = None
    hire_date_from: Optional[date] = None
    hire_date_to: Optional[date] = None
    
    @validator('hire_date_from', 'hire_date_to')
    def validate_date_range(cls, v, values):
        if 'hire_date_from' in values and 'hire_date_to' in values:
            if values['hire_date_from'] and values['hire_date_to']:
                if values['hire_date_from'] > values['hire_date_to']:
                    raise ValueError('Start date cannot be after end date')
        return v


class TeacherStats(BaseModel):
    """Schema for teacher statistics"""
    teacher_id: int
    full_name: str
    employee_id: str
    qualification: str
    specialization: str
    hire_date: date
    experience_years: float
    attendance_percentage: float
    total_attendance_days: int
    present_days: int
    status: str
    salary: Optional[float]
    emergency_contacts: Dict[str, Any]
    certificates: List[Dict[str, Any]]
    experience_details: List[Dict[str, Any]]


class TeacherAttendance(BaseModel):
    """Schema for teacher attendance records"""
    id: int
    date: date
    status: str
    method: str
    check_in_time: Optional[datetime]
    check_out_time: Optional[datetime]
    location: Optional[str]
    notes: Optional[str]


class TeacherBulkImportResult(BaseModel):
    """Schema for bulk import results"""
    total: int
    successful: int
    failed: int
    errors: List[Dict[str, Any]]


class TeacherExportRequest(BaseModel):
    """Schema for teacher export request"""
    format: str = Field("csv", regex="^(csv|excel|pdf)$")
    include_inactive: bool = False
    filters: Optional[TeacherSearch] = None