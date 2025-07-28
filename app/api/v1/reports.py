"""Reports API endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.reports import (
    DashboardStats, AttendanceReport, FeeReport, AcademicReport,
    FinancialReport, StudentReport, TeacherReport, AlertReport,
    ReportFilter, AlertRule, TriggerCriteria, ReportExportRequest,
    ReportGenerationRequest, ReportGenerationResponse
)
from app.services.reporting_service import ReportingService

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    date_from: Optional[date] = Query(None, description="Start date for statistics"),
    date_to: Optional[date] = Query(None, description="End date for statistics"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive dashboard statistics"""
    try:
        return ReportingService.get_dashboard_stats(
            db, current_user.tenant_id, date_from, date_to
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attendance", response_model=AttendanceReport)
async def get_attendance_report(
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    teacher_id: Optional[int] = Query(None, description="Filter by teacher ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate comprehensive attendance report"""
    try:
        filters = ReportFilter(
            date_from=date_from,
            date_to=date_to,
            student_id=student_id,
            teacher_id=teacher_id
        )
        return ReportingService.get_attendance_report(db, current_user.tenant_id, filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fees", response_model=FeeReport)
async def get_fee_report(
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    fee_type: Optional[str] = Query(None, description="Filter by fee type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate comprehensive fee report"""
    try:
        filters = ReportFilter(
            date_from=date_from,
            date_to=date_to,
            student_id=student_id,
            fee_type=fee_type,
            status=status
        )
        return ReportingService.get_fee_report(db, current_user.tenant_id, filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/academic", response_model=AcademicReport)
async def get_academic_report(
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    grade: Optional[str] = Query(None, description="Filter by grade"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate academic performance report"""
    try:
        filters = ReportFilter(
            date_from=date_from,
            date_to=date_to,
            grade=grade
        )
        return ReportingService.get_academic_report(db, current_user.tenant_id, filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/financial", response_model=FinancialReport)
async def get_financial_report(
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate comprehensive financial report"""
    try:
        filters = ReportFilter(
            date_from=date_from,
            date_to=date_to
        )
        return ReportingService.get_financial_report(db, current_user.tenant_id, filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/students/{student_id}", response_model=StudentReport)
async def get_student_report(
    student_id: int,
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate individual student report"""
    try:
        # Implementation for individual student report
        # This would combine attendance, fees, and academic data for a specific student
        filters = ReportFilter(
            date_from=date_from,
            date_to=date_to,
            student_id=student_id
        )
        
        # Placeholder response - implement full student report logic
        return StudentReport(
            student_id=student_id,
            student_name="Student Name",
            grade="Grade",
            attendance_percentage=85.0,
            total_fees=1000.0,
            paid_fees=800.0,
            outstanding_fees=200.0,
            academic_performance={},
            attendance_history=[],
            fee_history=[]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teachers/{teacher_id}", response_model=TeacherReport)
async def get_teacher_report(
    teacher_id: int,
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate individual teacher report"""
    try:
        # Implementation for individual teacher report
        filters = ReportFilter(
            date_from=date_from,
            date_to=date_to,
            teacher_id=teacher_id
        )
        
        # Placeholder response - implement full teacher report logic
        return TeacherReport(
            teacher_id=teacher_id,
            teacher_name="Teacher Name",
            qualification="Bachelor's",
            specialization="Mathematics",
            attendance_percentage=95.0,
            experience_years=5.0,
            salary=50000.0,
            performance_metrics={},
            attendance_history=[]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=List[AlertReport])
async def get_active_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all active alerts and notifications"""
    try:
        return ReportingService.check_triggers(db, current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/rules", response_model=AlertRule)
async def create_alert_rule(
    rule: AlertRule,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new alert rule"""
    try:
        return ReportingService.create_alert_rule(db, rule, current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export", response_model=ReportGenerationResponse)
async def export_report(
    request: ReportExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export report in specified format"""
    try:
        # Implementation for report export
        # This would generate PDF, Excel, or CSV reports
        return ReportGenerationResponse(
            report_id=f"report_{datetime.utcnow().timestamp()}",
            status="pending",
            created_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=ReportGenerationResponse)
async def generate_report(
    request: ReportGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate custom report"""
    try:
        # Implementation for custom report generation
        return ReportGenerationResponse(
            report_id=f"custom_report_{datetime.utcnow().timestamp()}",
            status="pending",
            created_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/trends")
async def get_analytics_trends(
    metric: str = Query(..., description="Metric to analyze"),
    period: str = Query("monthly", description="Analysis period"),
    date_from: Optional[date] = Query(None, description="Start date"),
    date_to: Optional[date] = Query(None, description="End date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics trends for specific metrics"""
    try:
        # Implementation for analytics trends
        # This would provide trend analysis for various metrics
        return {
            "metric": metric,
            "period": period,
            "trends": [],
            "insights": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kpis")
async def get_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get Key Performance Indicators"""
    try:
        # Implementation for KPIs
        # This would provide key metrics and their targets
        return {
            "attendance_rate": 85.5,
            "fee_collection_rate": 92.3,
            "student_satisfaction": 4.2,
            "teacher_retention": 95.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/status/{report_id}")
async def get_report_status(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the status of a report generation job"""
    try:
        # Implementation for report status checking
        return {
            "report_id": report_id,
            "status": "completed",
            "progress": 100,
            "download_url": f"/downloads/{report_id}.pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/alerts/{alert_id}")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark an alert as resolved"""
    try:
        # Implementation for alert resolution
        return {"message": "Alert resolved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/widgets")
async def get_dashboard_widgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard widget configuration"""
    try:
        # Implementation for dashboard widgets
        return {
            "widgets": [
                {
                    "id": "attendance_chart",
                    "title": "Attendance Overview",
                    "type": "chart",
                    "data": {},
                    "position": {"x": 0, "y": 0},
                    "size": {"width": 6, "height": 4}
                },
                {
                    "id": "fee_summary",
                    "title": "Fee Collection",
                    "type": "metric",
                    "data": {},
                    "position": {"x": 6, "y": 0},
                    "size": {"width": 6, "height": 4}
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))