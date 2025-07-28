from typing import Optional, List, Dict, Any
from datetime import date, datetime, time
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.models.attendance import AttendanceStatus, AttendanceMethod


class AttendanceStatusEnum(str, Enum):
    """Attendance status options"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    LEAVE = "leave"
    HALF_DAY = "half_day"


class AttendanceMethodEnum(str, Enum):
    """Attendance method options"""
    MANUAL = "manual"
    QR_SCANNER = "qr_scanner"
    GEOLOCATION = "geolocation"
    BIOMETRIC = "biometric"
    CARD_SWIPE = "card_swipe"


class AttendanceMarkRequest(BaseModel):
    """Schema for marking attendance"""
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    date: date = Field(default_factory=date.today)
    status: AttendanceStatusEnum
    method: AttendanceMethodEnum = AttendanceMethodEnum.MANUAL
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('student_id', 'teacher_id')
    def validate_person_id(cls, v, values):
        if 'student_id' in values and 'teacher_id' in values:
            if values['student_id'] is None and values['teacher_id'] is None:
                raise ValueError("Either student_id or teacher_id must be provided")
            if values['student_id'] is not None and values['teacher_id'] is not None:
                raise ValueError("Cannot provide both student_id and teacher_id")
        return v
    
    @validator('date')
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError("Cannot mark attendance for future dates")
        return v


class AttendanceCreate(BaseModel):
    """Schema for creating attendance record"""
    tenant_id: int
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    date: date
    status: AttendanceStatusEnum
    method: AttendanceMethodEnum
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=500)
    marked_by: int
    
    @validator('student_id', 'teacher_id')
    def validate_person_id(cls, v, values):
        if 'student_id' in values and 'teacher_id' in values:
            if values['student_id'] is None and values['teacher_id'] is None:
                raise ValueError("Either student_id or teacher_id must be provided")
            if values['student_id'] is not None and values['teacher_id'] is not None:
                raise ValueError("Cannot provide both student_id and teacher_id")
        return v


class AttendanceResponse(BaseModel):
    """Schema for attendance response data"""
    id: int
    tenant_id: int
    student_id: Optional[int]
    teacher_id: Optional[int]
    date: date
    status: AttendanceStatusEnum
    method: AttendanceMethodEnum
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    location: Optional[str]
    notes: Optional[str]
    marked_by: int
    created_at: datetime
    updated_at: datetime
    
    # Related data
    student_name: Optional[str] = None
    teacher_name: Optional[str] = None
    marked_by_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class AttendanceList(BaseModel):
    """Schema for paginated attendance list"""
    records: List[AttendanceResponse]
    total: int
    skip: int
    limit: int


class AttendanceSearch(BaseModel):
    """Schema for attendance search parameters"""
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    status: Optional[AttendanceStatusEnum] = None
    method: Optional[AttendanceMethodEnum] = None
    
    @validator('date_from', 'date_to')
    def validate_date_range(cls, v, values):
        if 'date_from' in values and 'date_to' in values:
            if values['date_from'] and values['date_to']:
                if values['date_from'] > values['date_to']:
                    raise ValueError('Start date cannot be after end date')
        return v


class AttendanceStats(BaseModel):
    """Schema for attendance statistics"""
    total_records: int
    present_count: int
    absent_count: int
    late_count: int
    leave_count: int
    present_percentage: float
    absent_percentage: float
    late_percentage: float
    leave_percentage: float


class QRCodeCreate(BaseModel):
    """Schema for creating QR code"""
    code: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=200)
    valid_from: datetime
    valid_until: datetime
    max_usage: int = Field(..., ge=1)
    location: Optional[str] = Field(None, max_length=100)
    created_by: int
    
    @validator('valid_until')
    def validate_valid_until(cls, v, values):
        if 'valid_from' in values and values['valid_from'] >= v:
            raise ValueError('Valid until must be after valid from')
        return v
    
    @validator('max_usage')
    def validate_max_usage(cls, v):
        if v <= 0:
            raise ValueError('Max usage must be greater than 0')
        return v


class QRCodeResponse(BaseModel):
    """Schema for QR code response data"""
    id: int
    code: str
    description: str
    valid_from: datetime
    valid_until: datetime
    max_usage: int
    current_usage: int
    location: Optional[str]
    is_active: bool
    created_at: datetime
    qr_image: str  # Base64 encoded image
    
    class Config:
        from_attributes = True


class QRCodeVerifyRequest(BaseModel):
    """Schema for QR code verification request"""
    qr_code: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)


class GeolocationAttendanceRequest(BaseModel):
    """Schema for geolocation attendance request"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=200)
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if v < -90 or v > 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if v < -180 or v > 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v


class AttendanceScheduleCreate(BaseModel):
    """Schema for creating attendance schedule"""
    tenant_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: time
    end_time: time
    days_of_week: List[int] = Field(..., min_items=1, max_items=7)  # 0=Monday, 6=Sunday
    is_active: bool = True
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and values['start_time'] >= v:
            raise ValueError('End time must be after start time')
        return v
    
    @validator('days_of_week')
    def validate_days_of_week(cls, v):
        for day in v:
            if day < 0 or day > 6:
                raise ValueError('Days of week must be between 0 and 6')
        return v


class AttendanceScheduleResponse(BaseModel):
    """Schema for attendance schedule response"""
    id: int
    tenant_id: int
    name: str
    description: Optional[str]
    start_time: time
    end_time: time
    days_of_week: List[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AttendanceBulkMarkRequest(BaseModel):
    """Schema for bulk marking attendance"""
    records: List[AttendanceMarkRequest] = Field(..., min_items=1, max_items=100)
    
    @validator('records')
    def validate_records(cls, v):
        if len(v) > 100:
            raise ValueError('Cannot mark more than 100 records at once')
        return v


class AttendanceBulkMarkResponse(BaseModel):
    """Schema for bulk attendance marking response"""
    total: int
    successful: int
    failed: int
    errors: List[Dict[str, Any]]


class AttendanceExportRequest(BaseModel):
    """Schema for attendance export request"""
    format: str = Field("csv", regex="^(csv|excel|pdf)$")
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    status: Optional[AttendanceStatusEnum] = None
    include_details: bool = True
    
    @validator('date_from', 'date_to')
    def validate_date_range(cls, v, values):
        if 'date_from' in values and 'date_to' in values:
            if values['date_from'] and values['date_to']:
                if values['date_from'] > values['date_to']:
                    raise ValueError('Start date cannot be after end date')
        return v