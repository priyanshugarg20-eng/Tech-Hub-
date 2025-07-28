from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, extract, case
from datetime import datetime, date, timedelta
import logging
from decimal import Decimal

from app.models.student import Student, StudentStatus
from app.models.teacher import Teacher, TeacherStatus
from app.models.attendance import AttendanceRecord, AttendanceStatus
from app.models.fees import FeeRecord, Payment, PaymentStatus
from app.models.tenant import Tenant
from app.schemas.reports import (
    DashboardStats, AttendanceReport, FeeReport, AcademicReport,
    StudentReport, TeacherReport, FinancialReport, AlertReport,
    TriggerCriteria, AlertRule, ReportFilter
)
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class ReportingService:
    """Service class for comprehensive reporting and dashboard analytics"""
    
    @staticmethod
    def get_dashboard_stats(
        db: Session,
        tenant_id: int,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> DashboardStats:
        """Get comprehensive dashboard statistics"""
        try:
            if not date_from:
                date_from = date.today() - timedelta(days=30)
            if not date_to:
                date_to = date.today()
            
            # Student statistics
            total_students = db.query(Student).filter(
                and_(Student.tenant_id == tenant_id, Student.status == StudentStatus.ACTIVE)
            ).count()
            
            new_students_this_month = db.query(Student).filter(
                and_(
                    Student.tenant_id == tenant_id,
                    Student.created_at >= date_from,
                    Student.status == StudentStatus.ACTIVE
                )
            ).count()
            
            # Teacher statistics
            total_teachers = db.query(Teacher).filter(
                and_(Teacher.tenant_id == tenant_id, Teacher.status == TeacherStatus.ACTIVE)
            ).count()
            
            # Attendance statistics
            attendance_stats = ReportingService._get_attendance_stats(db, tenant_id, date_from, date_to)
            
            # Fee statistics
            fee_stats = ReportingService._get_fee_stats(db, tenant_id, date_from, date_to)
            
            # Academic performance
            academic_stats = ReportingService._get_academic_stats(db, tenant_id, date_from, date_to)
            
            # Recent activities
            recent_activities = ReportingService._get_recent_activities(db, tenant_id, limit=10)
            
            # Alerts and notifications
            alerts = ReportingService._get_active_alerts(db, tenant_id)
            
            return DashboardStats(
                total_students=total_students,
                new_students_this_month=new_students_this_month,
                total_teachers=total_teachers,
                attendance_stats=attendance_stats,
                fee_stats=fee_stats,
                academic_stats=academic_stats,
                recent_activities=recent_activities,
                alerts=alerts
            )
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {str(e)}")
            raise
    
    @staticmethod
    def get_attendance_report(
        db: Session,
        tenant_id: int,
        filters: ReportFilter
    ) -> AttendanceReport:
        """Generate comprehensive attendance report"""
        try:
            query = db.query(AttendanceRecord).filter(AttendanceRecord.tenant_id == tenant_id)
            
            if filters.date_from:
                query = query.filter(AttendanceRecord.date >= filters.date_from)
            if filters.date_to:
                query = query.filter(AttendanceRecord.date <= filters.date_to)
            if filters.student_id:
                query = query.filter(AttendanceRecord.student_id == filters.student_id)
            if filters.teacher_id:
                query = query.filter(AttendanceRecord.teacher_id == filters.teacher_id)
            
            # Daily attendance trends
            daily_trends = db.query(
                AttendanceRecord.date,
                func.count(AttendanceRecord.id).label('total'),
                func.sum(case([(AttendanceRecord.status == AttendanceStatus.PRESENT, 1)], else_=0)).label('present'),
                func.sum(case([(AttendanceRecord.status == AttendanceStatus.ABSENT, 1)], else_=0)).label('absent'),
                func.sum(case([(AttendanceRecord.status == AttendanceStatus.LATE, 1)], else_=0)).label('late')
            ).filter(
                and_(
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= filters.date_from,
                    AttendanceRecord.date <= filters.date_to
                )
            ).group_by(AttendanceRecord.date).order_by(AttendanceRecord.date).all()
            
            # Attendance by method
            method_stats = db.query(
                AttendanceRecord.method,
                func.count(AttendanceRecord.id).label('count')
            ).filter(
                and_(
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= filters.date_from,
                    AttendanceRecord.date <= filters.date_to
                )
            ).group_by(AttendanceRecord.method).all()
            
            # Top absent students
            absent_students = db.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                func.count(AttendanceRecord.id).label('absent_count')
            ).join(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.status == AttendanceStatus.ABSENT,
                    AttendanceRecord.date >= filters.date_from,
                    AttendanceRecord.date <= filters.date_to
                )
            ).group_by(Student.id, Student.first_name, Student.last_name).order_by(
                desc('absent_count')
            ).limit(10).all()
            
            return AttendanceReport(
                total_records=query.count(),
                daily_trends=daily_trends,
                method_stats=method_stats,
                absent_students=absent_students,
                overall_attendance_rate=ReportingService._calculate_attendance_rate(db, tenant_id, filters)
            )
            
        except Exception as e:
            logger.error(f"Error generating attendance report: {str(e)}")
            raise
    
    @staticmethod
    def get_fee_report(
        db: Session,
        tenant_id: int,
        filters: ReportFilter
    ) -> FeeReport:
        """Generate comprehensive fee report"""
        try:
            # Fee collection statistics
            fee_stats = db.query(
                func.sum(FeeRecord.amount).label('total_fees'),
                func.sum(case([(FeeRecord.status == PaymentStatus.PAID, FeeRecord.amount)], else_=0)).label('collected'),
                func.sum(case([(FeeRecord.status == PaymentStatus.PENDING, FeeRecord.amount)], else_=0)).label('pending'),
                func.sum(case([(FeeRecord.status == PaymentStatus.OVERDUE, FeeRecord.amount)], else_=0)).label('overdue')
            ).filter(
                and_(
                    FeeRecord.tenant_id == tenant_id,
                    FeeRecord.due_date >= filters.date_from,
                    FeeRecord.due_date <= filters.date_to
                )
            ).first()
            
            # Monthly collection trends
            monthly_collection = db.query(
                extract('month', Payment.payment_date).label('month'),
                extract('year', Payment.payment_date).label('year'),
                func.sum(Payment.amount).label('total_collected')
            ).filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.payment_date >= filters.date_from,
                    Payment.payment_date <= filters.date_to
                )
            ).group_by(
                extract('month', Payment.payment_date),
                extract('year', Payment.payment_date)
            ).order_by('year', 'month').all()
            
            # Payment method distribution
            payment_methods = db.query(
                Payment.payment_method,
                func.count(Payment.id).label('count'),
                func.sum(Payment.amount).label('total_amount')
            ).filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.payment_date >= filters.date_from,
                    Payment.payment_date <= filters.date_to
                )
            ).group_by(Payment.payment_method).all()
            
            # Top defaulters
            defaulters = db.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                func.sum(FeeRecord.amount).label('total_due'),
                func.sum(case([(FeeRecord.status == PaymentStatus.OVERDUE, FeeRecord.amount)], else_=0)).label('overdue_amount')
            ).join(FeeRecord).filter(
                and_(
                    FeeRecord.tenant_id == tenant_id,
                    FeeRecord.status.in_([PaymentStatus.PENDING, PaymentStatus.OVERDUE])
                )
            ).group_by(Student.id, Student.first_name, Student.last_name).order_by(
                desc('overdue_amount')
            ).limit(10).all()
            
            return FeeReport(
                total_fees=float(fee_stats.total_fees or 0),
                collected_amount=float(fee_stats.collected or 0),
                pending_amount=float(fee_stats.pending or 0),
                overdue_amount=float(fee_stats.overdue or 0),
                collection_rate=round((fee_stats.collected / fee_stats.total_fees * 100) if fee_stats.total_fees else 0, 2),
                monthly_collection=monthly_collection,
                payment_methods=payment_methods,
                defaulters=defaulters
            )
            
        except Exception as e:
            logger.error(f"Error generating fee report: {str(e)}")
            raise
    
    @staticmethod
    def get_academic_report(
        db: Session,
        tenant_id: int,
        filters: ReportFilter
    ) -> AcademicReport:
        """Generate academic performance report"""
        try:
            # Grade distribution
            grade_distribution = db.query(
                Student.grade,
                func.count(Student.id).label('student_count')
            ).filter(
                and_(
                    Student.tenant_id == tenant_id,
                    Student.status == StudentStatus.ACTIVE
                )
            ).group_by(Student.grade).all()
            
            # Performance trends (placeholder for LMS integration)
            performance_trends = []
            
            # Top performing students
            top_students = db.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                Student.grade,
                Student.attendance_percentage
            ).filter(
                and_(
                    Student.tenant_id == tenant_id,
                    Student.status == StudentStatus.ACTIVE
                )
            ).order_by(desc(Student.attendance_percentage)).limit(10).all()
            
            # Class-wise statistics
            class_stats = db.query(
                Student.grade,
                func.count(Student.id).label('total_students'),
                func.avg(Student.attendance_percentage).label('avg_attendance'),
                func.sum(case([(Student.attendance_percentage >= 90, 1)], else_=0)).label('excellent_attendance')
            ).filter(
                and_(
                    Student.tenant_id == tenant_id,
                    Student.status == StudentStatus.ACTIVE
                )
            ).group_by(Student.grade).all()
            
            return AcademicReport(
                grade_distribution=grade_distribution,
                performance_trends=performance_trends,
                top_students=top_students,
                class_stats=class_stats
            )
            
        except Exception as e:
            logger.error(f"Error generating academic report: {str(e)}")
            raise
    
    @staticmethod
    def get_financial_report(
        db: Session,
        tenant_id: int,
        filters: ReportFilter
    ) -> FinancialReport:
        """Generate comprehensive financial report"""
        try:
            # Revenue analysis
            revenue_stats = db.query(
                func.sum(Payment.amount).label('total_revenue'),
                func.avg(Payment.amount).label('avg_payment'),
                func.count(Payment.id).label('total_transactions')
            ).filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.payment_date >= filters.date_from,
                    Payment.payment_date <= filters.date_to
                )
            ).first()
            
            # Expense tracking (placeholder for future implementation)
            expenses = []
            
            # Cash flow analysis
            cash_flow = db.query(
                extract('month', Payment.payment_date).label('month'),
                extract('year', Payment.payment_date).label('year'),
                func.sum(Payment.amount).label('inflow'),
                func.count(Payment.id).label('transactions')
            ).filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.payment_date >= filters.date_from,
                    Payment.payment_date <= filters.date_to
                )
            ).group_by(
                extract('month', Payment.payment_date),
                extract('year', Payment.payment_date)
            ).order_by('year', 'month').all()
            
            # Outstanding receivables
            outstanding = db.query(
                func.sum(FeeRecord.amount).label('total_outstanding'),
                func.count(FeeRecord.id).label('outstanding_count')
            ).filter(
                and_(
                    FeeRecord.tenant_id == tenant_id,
                    FeeRecord.status.in_([PaymentStatus.PENDING, PaymentStatus.OVERDUE])
                )
            ).first()
            
            return FinancialReport(
                total_revenue=float(revenue_stats.total_revenue or 0),
                avg_payment=float(revenue_stats.avg_payment or 0),
                total_transactions=revenue_stats.total_transactions or 0,
                expenses=expenses,
                cash_flow=cash_flow,
                outstanding_amount=float(outstanding.total_outstanding or 0),
                outstanding_count=outstanding.outstanding_count or 0
            )
            
        except Exception as e:
            logger.error(f"Error generating financial report: {str(e)}")
            raise
    
    @staticmethod
    def create_alert_rule(
        db: Session,
        rule_data: AlertRule,
        tenant_id: int
    ) -> AlertRule:
        """Create a new alert rule"""
        try:
            # Implementation for alert rules
            # This would typically involve creating a new table for alert rules
            # For now, we'll return the rule data
            return rule_data
            
        except Exception as e:
            logger.error(f"Error creating alert rule: {str(e)}")
            raise
    
    @staticmethod
    def check_triggers(
        db: Session,
        tenant_id: int
    ) -> List[AlertReport]:
        """Check for triggered alerts based on criteria"""
        try:
            alerts = []
            
            # Check attendance triggers
            attendance_alerts = ReportingService._check_attendance_triggers(db, tenant_id)
            alerts.extend(attendance_alerts)
            
            # Check fee triggers
            fee_alerts = ReportingService._check_fee_triggers(db, tenant_id)
            alerts.extend(fee_alerts)
            
            # Check academic triggers
            academic_alerts = ReportingService._check_academic_triggers(db, tenant_id)
            alerts.extend(academic_alerts)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking triggers: {str(e)}")
            raise
    
    @staticmethod
    def _get_attendance_stats(db: Session, tenant_id: int, date_from: date, date_to: date) -> Dict[str, Any]:
        """Get attendance statistics for dashboard"""
        try:
            total_records = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= date_from,
                    AttendanceRecord.date <= date_to
                )
            ).count()
            
            present_count = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= date_from,
                    AttendanceRecord.date <= date_to,
                    AttendanceRecord.status == AttendanceStatus.PRESENT
                )
            ).count()
            
            attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
            
            return {
                "total_records": total_records,
                "present_count": present_count,
                "attendance_rate": round(attendance_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting attendance stats: {str(e)}")
            return {"total_records": 0, "present_count": 0, "attendance_rate": 0}
    
    @staticmethod
    def _get_fee_stats(db: Session, tenant_id: int, date_from: date, date_to: date) -> Dict[str, Any]:
        """Get fee statistics for dashboard"""
        try:
            total_fees = db.query(FeeRecord).filter(
                and_(
                    FeeRecord.tenant_id == tenant_id,
                    FeeRecord.due_date >= date_from,
                    FeeRecord.due_date <= date_to
                )
            ).with_entities(func.sum(FeeRecord.amount)).scalar() or 0
            
            collected_amount = db.query(Payment).filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.payment_date >= date_from,
                    Payment.payment_date <= date_to
                )
            ).with_entities(func.sum(Payment.amount)).scalar() or 0
            
            collection_rate = (collected_amount / total_fees * 100) if total_fees > 0 else 0
            
            return {
                "total_fees": float(total_fees),
                "collected_amount": float(collected_amount),
                "collection_rate": round(collection_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting fee stats: {str(e)}")
            return {"total_fees": 0, "collected_amount": 0, "collection_rate": 0}
    
    @staticmethod
    def _get_academic_stats(db: Session, tenant_id: int, date_from: date, date_to: date) -> Dict[str, Any]:
        """Get academic statistics for dashboard"""
        try:
            total_students = db.query(Student).filter(
                and_(Student.tenant_id == tenant_id, Student.status == StudentStatus.ACTIVE)
            ).count()
            
            avg_attendance = db.query(func.avg(Student.attendance_percentage)).filter(
                and_(Student.tenant_id == tenant_id, Student.status == StudentStatus.ACTIVE)
            ).scalar() or 0
            
            return {
                "total_students": total_students,
                "avg_attendance": round(avg_attendance, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting academic stats: {str(e)}")
            return {"total_students": 0, "avg_attendance": 0}
    
    @staticmethod
    def _get_recent_activities(db: Session, tenant_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities for dashboard"""
        try:
            activities = []
            
            # Recent attendance records
            recent_attendance = db.query(AttendanceRecord).filter(
                AttendanceRecord.tenant_id == tenant_id
            ).order_by(desc(AttendanceRecord.created_at)).limit(limit).all()
            
            for record in recent_attendance:
                activities.append({
                    "type": "attendance",
                    "description": f"Attendance marked for {record.student.full_name if record.student else record.teacher.full_name}",
                    "timestamp": record.created_at,
                    "status": record.status
                })
            
            # Recent payments
            recent_payments = db.query(Payment).filter(
                Payment.tenant_id == tenant_id
            ).order_by(desc(Payment.created_at)).limit(limit).all()
            
            for payment in recent_payments:
                activities.append({
                    "type": "payment",
                    "description": f"Payment of ${payment.amount} received",
                    "timestamp": payment.created_at,
                    "status": "completed"
                })
            
            # Sort by timestamp and return top activities
            activities.sort(key=lambda x: x["timestamp"], reverse=True)
            return activities[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent activities: {str(e)}")
            return []
    
    @staticmethod
    def _get_active_alerts(db: Session, tenant_id: int) -> List[Dict[str, Any]]:
        """Get active alerts for dashboard"""
        try:
            alerts = []
            
            # Check for overdue fees
            overdue_count = db.query(FeeRecord).filter(
                and_(
                    FeeRecord.tenant_id == tenant_id,
                    FeeRecord.status == PaymentStatus.OVERDUE
                )
            ).count()
            
            if overdue_count > 0:
                alerts.append({
                    "type": "warning",
                    "title": "Overdue Fees",
                    "message": f"{overdue_count} fees are overdue",
                    "count": overdue_count
                })
            
            # Check for low attendance
            low_attendance_students = db.query(Student).filter(
                and_(
                    Student.tenant_id == tenant_id,
                    Student.attendance_percentage < 75,
                    Student.status == StudentStatus.ACTIVE
                )
            ).count()
            
            if low_attendance_students > 0:
                alerts.append({
                    "type": "warning",
                    "title": "Low Attendance",
                    "message": f"{low_attendance_students} students have low attendance",
                    "count": low_attendance_students
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting active alerts: {str(e)}")
            return []
    
    @staticmethod
    def _calculate_attendance_rate(db: Session, tenant_id: int, filters: ReportFilter) -> float:
        """Calculate overall attendance rate"""
        try:
            query = db.query(AttendanceRecord).filter(AttendanceRecord.tenant_id == tenant_id)
            
            if filters.date_from:
                query = query.filter(AttendanceRecord.date >= filters.date_from)
            if filters.date_to:
                query = query.filter(AttendanceRecord.date <= filters.date_to)
            
            total_records = query.count()
            present_records = query.filter(AttendanceRecord.status == AttendanceStatus.PRESENT).count()
            
            return round((present_records / total_records * 100) if total_records > 0 else 0, 2)
            
        except Exception as e:
            logger.error(f"Error calculating attendance rate: {str(e)}")
            return 0.0
    
    @staticmethod
    def _check_attendance_triggers(db: Session, tenant_id: int) -> List[AlertReport]:
        """Check attendance-based triggers"""
        alerts = []
        
        # Students with consecutive absences
        students_with_absences = db.query(Student).filter(
            and_(
                Student.tenant_id == tenant_id,
                Student.attendance_percentage < 80,
                Student.status == StudentStatus.ACTIVE
            )
        ).all()
        
        for student in students_with_absences:
            alerts.append(AlertReport(
                type="attendance",
                severity="medium",
                title="Low Attendance Alert",
                message=f"Student {student.full_name} has {100 - student.attendance_percentage}% absence rate",
                student_id=student.id,
                teacher_id=None,
                fee_id=None
            ))
        
        return alerts
    
    @staticmethod
    def _check_fee_triggers(db: Session, tenant_id: int) -> List[AlertReport]:
        """Check fee-based triggers"""
        alerts = []
        
        # Overdue fees
        overdue_fees = db.query(FeeRecord).filter(
            and_(
                FeeRecord.tenant_id == tenant_id,
                FeeRecord.status == PaymentStatus.OVERDUE
            )
        ).all()
        
        for fee in overdue_fees:
            alerts.append(AlertReport(
                type="fee",
                severity="high",
                title="Overdue Fee Alert",
                message=f"Fee of ${fee.amount} is overdue for {fee.student.full_name}",
                student_id=fee.student_id,
                teacher_id=None,
                fee_id=fee.id
            ))
        
        return alerts
    
    @staticmethod
    def _check_academic_triggers(db: Session, tenant_id: int) -> List[AlertReport]:
        """Check academic-based triggers"""
        alerts = []
        
        # Students with very low attendance
        critical_attendance = db.query(Student).filter(
            and_(
                Student.tenant_id == tenant_id,
                Student.attendance_percentage < 60,
                Student.status == StudentStatus.ACTIVE
            )
        ).all()
        
        for student in critical_attendance:
            alerts.append(AlertReport(
                type="academic",
                severity="high",
                title="Critical Attendance Alert",
                message=f"Student {student.full_name} has critical attendance rate of {student.attendance_percentage}%",
                student_id=student.id,
                teacher_id=None,
                fee_id=None
            ))
        
        return alerts