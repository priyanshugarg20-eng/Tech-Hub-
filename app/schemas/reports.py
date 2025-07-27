from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class ReportTypeEnum(str, Enum):
    """Report type options"""
    ATTENDANCE = "attendance"
    FEE = "fee"
    ACADEMIC = "academic"
    FINANCIAL = "financial"
    STUDENT = "student"
    TEACHER = "teacher"


class AlertSeverityEnum(str, Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertTypeEnum(str, Enum):
    """Alert type options"""
    ATTENDANCE = "attendance"
    FEE = "fee"
    ACADEMIC = "academic"
    SYSTEM = "system"


class ReportFilter(BaseModel):
    """Schema for report filtering"""
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    grade: Optional[str] = None
    fee_type: Optional[str] = None
    status: Optional[str] = None
    
    @validator('date_from', 'date_to')
    def validate_date_range(cls, v, values):
        if 'date_from' in values and 'date_to' in values:
            if values['date_from'] and values['date_to']:
                if values['date_from'] > values['date_to']:
                    raise ValueError('Start date cannot be after end date')
        return v


class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    total_students: int
    new_students_this_month: int
    total_teachers: int
    attendance_stats: Dict[str, Any]
    fee_stats: Dict[str, Any]
    academic_stats: Dict[str, Any]
    recent_activities: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]


class AttendanceReport(BaseModel):
    """Schema for attendance report"""
    total_records: int
    daily_trends: List[Dict[str, Any]]
    method_stats: List[Dict[str, Any]]
    absent_students: List[Dict[str, Any]]
    overall_attendance_rate: float


class FeeReport(BaseModel):
    """Schema for fee report"""
    total_fees: float
    collected_amount: float
    pending_amount: float
    overdue_amount: float
    collection_rate: float
    monthly_collection: List[Dict[str, Any]]
    payment_methods: List[Dict[str, Any]]
    defaulters: List[Dict[str, Any]]


class AcademicReport(BaseModel):
    """Schema for academic report"""
    grade_distribution: List[Dict[str, Any]]
    performance_trends: List[Dict[str, Any]]
    top_students: List[Dict[str, Any]]
    class_stats: List[Dict[str, Any]]


class FinancialReport(BaseModel):
    """Schema for financial report"""
    total_revenue: float
    avg_payment: float
    total_transactions: int
    expenses: List[Dict[str, Any]]
    cash_flow: List[Dict[str, Any]]
    outstanding_amount: float
    outstanding_count: int


class StudentReport(BaseModel):
    """Schema for student report"""
    student_id: int
    student_name: str
    grade: str
    attendance_percentage: float
    total_fees: float
    paid_fees: float
    outstanding_fees: float
    academic_performance: Dict[str, Any]
    attendance_history: List[Dict[str, Any]]
    fee_history: List[Dict[str, Any]]


class TeacherReport(BaseModel):
    """Schema for teacher report"""
    teacher_id: int
    teacher_name: str
    qualification: str
    specialization: str
    attendance_percentage: float
    experience_years: float
    salary: float
    performance_metrics: Dict[str, Any]
    attendance_history: List[Dict[str, Any]]


class AlertReport(BaseModel):
    """Schema for alert report"""
    type: AlertTypeEnum
    severity: AlertSeverityEnum
    title: str
    message: str
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    fee_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None


class TriggerCriteria(BaseModel):
    """Schema for trigger criteria"""
    attendance_threshold: Optional[float] = Field(None, ge=0, le=100)
    consecutive_absences: Optional[int] = Field(None, ge=1)
    fee_overdue_days: Optional[int] = Field(None, ge=1)
    low_grade_threshold: Optional[float] = Field(None, ge=0, le=100)
    payment_delay_days: Optional[int] = Field(None, ge=1)
    academic_performance_threshold: Optional[float] = Field(None, ge=0, le=100)


class AlertRule(BaseModel):
    """Schema for alert rule"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: AlertTypeEnum
    severity: AlertSeverityEnum
    criteria: TriggerCriteria
    is_active: bool = True
    notification_channels: List[str] = Field(default_factory=list)  # email, sms, push
    created_by: int


class ReportExportRequest(BaseModel):
    """Schema for report export request"""
    report_type: ReportTypeEnum
    format: str = Field("pdf", regex="^(pdf|excel|csv)$")
    filters: ReportFilter
    include_charts: bool = True
    include_details: bool = True


class DashboardWidget(BaseModel):
    """Schema for dashboard widget"""
    id: str
    title: str
    type: str  # chart, metric, table, alert
    data: Dict[str, Any]
    position: Dict[str, int]  # x, y coordinates
    size: Dict[str, int]  # width, height
    is_visible: bool = True
    refresh_interval: Optional[int] = None  # seconds


class DashboardConfig(BaseModel):
    """Schema for dashboard configuration"""
    tenant_id: int
    widgets: List[DashboardWidget]
    layout: Dict[str, Any]
    theme: str = "default"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ReportSchedule(BaseModel):
    """Schema for scheduled reports"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    report_type: ReportTypeEnum
    filters: ReportFilter
    frequency: str = Field(..., regex="^(daily|weekly|monthly|quarterly)$")
    recipients: List[str] = Field(..., min_items=1)  # email addresses
    format: str = Field("pdf", regex="^(pdf|excel|csv)$")
    is_active: bool = True
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None


class AnalyticsData(BaseModel):
    """Schema for analytics data"""
    date: date
    metric: str
    value: float
    target: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None


class TrendAnalysis(BaseModel):
    """Schema for trend analysis"""
    metric: str
    current_value: float
    previous_value: float
    change_percentage: float
    trend_direction: str  # up, down, stable
    period: str  # daily, weekly, monthly
    data_points: List[AnalyticsData]


class KPI(BaseModel):
    """Schema for Key Performance Indicator"""
    name: str
    value: float
    target: Optional[float] = None
    unit: str
    trend: Optional[TrendAnalysis] = None
    status: str  # good, warning, critical
    description: Optional[str] = None


class DashboardSummary(BaseModel):
    """Schema for dashboard summary"""
    kpis: List[KPI]
    trends: List[TrendAnalysis]
    alerts: List[AlertReport]
    recent_activities: List[Dict[str, Any]]
    quick_actions: List[Dict[str, Any]]


class ReportTemplate(BaseModel):
    """Schema for report template"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    report_type: ReportTypeEnum
    template_data: Dict[str, Any]
    is_default: bool = False
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ReportGenerationRequest(BaseModel):
    """Schema for report generation request"""
    report_type: ReportTypeEnum
    template_id: Optional[int] = None
    filters: ReportFilter
    format: str = Field("pdf", regex="^(pdf|excel|csv|html)$")
    include_charts: bool = True
    include_summary: bool = True
    custom_parameters: Optional[Dict[str, Any]] = None


class ReportGenerationResponse(BaseModel):
    """Schema for report generation response"""
    report_id: str
    status: str  # pending, processing, completed, failed
    download_url: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None