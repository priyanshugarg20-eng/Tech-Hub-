from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, date, time
import logging
import qrcode
import io
import base64
from geopy.distance import geodesic

from app.models.attendance import AttendanceRecord, QRCode, AttendanceSchedule, AttendanceStatus, AttendanceMethod
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User
from app.schemas.attendance import (
    AttendanceCreate, AttendanceResponse, AttendanceList, 
    QRCodeCreate, QRCodeResponse, AttendanceMarkRequest,
    AttendanceStats, AttendanceSearch
)
from app.services.notification_service import NotificationService
from app.core.config import settings

logger = logging.getLogger(__name__)


class AttendanceService:
    """Service class for attendance management operations"""
    
    @staticmethod
    def mark_attendance(
        db: Session,
        attendance_data: AttendanceMarkRequest,
        tenant_id: int,
        user_id: int
    ) -> AttendanceRecord:
        """Mark attendance for a student or teacher"""
        try:
            # Determine if it's a student or teacher
            student = None
            teacher = None
            
            if attendance_data.student_id:
                student = db.query(Student).filter(
                    and_(Student.id == attendance_data.student_id, Student.tenant_id == tenant_id)
                ).first()
                if not student:
                    raise ValueError("Student not found")
                person_id = student.id
                person_type = "student"
            elif attendance_data.teacher_id:
                teacher = db.query(Teacher).filter(
                    and_(Teacher.id == attendance_data.teacher_id, Teacher.tenant_id == tenant_id)
                ).first()
                if not teacher:
                    raise ValueError("Teacher not found")
                person_id = teacher.id
                person_type = "teacher"
            else:
                raise ValueError("Either student_id or teacher_id must be provided")
            
            # Check if attendance already exists for today
            existing_attendance = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date == attendance_data.date,
                    AttendanceRecord.student_id == attendance_data.student_id,
                    AttendanceRecord.teacher_id == attendance_data.teacher_id
                )
            ).first()
            
            if existing_attendance:
                # Update existing attendance
                existing_attendance.status = attendance_data.status
                existing_attendance.method = attendance_data.method
                existing_attendance.check_in_time = attendance_data.check_in_time or datetime.now().time()
                existing_attendance.check_out_time = attendance_data.check_out_time
                existing_attendance.location = attendance_data.location
                existing_attendance.notes = attendance_data.notes
                existing_attendance.updated_at = datetime.utcnow()
                
                attendance_record = existing_attendance
            else:
                # Create new attendance record
                attendance_record = AttendanceRecord(
                    tenant_id=tenant_id,
                    student_id=attendance_data.student_id,
                    teacher_id=attendance_data.teacher_id,
                    date=attendance_data.date,
                    status=attendance_data.status,
                    method=attendance_data.method,
                    check_in_time=attendance_data.check_in_time or datetime.now().time(),
                    check_out_time=attendance_data.check_out_time,
                    location=attendance_data.location,
                    notes=attendance_data.notes,
                    marked_by=user_id
                )
                db.add(attendance_record)
            
            db.commit()
            db.refresh(attendance_record)
            
            # Update attendance percentage for student/teacher
            if student:
                AttendanceService._update_student_attendance_percentage(db, student.id, tenant_id)
            elif teacher:
                AttendanceService._update_teacher_attendance_percentage(db, teacher.id, tenant_id)
            
            # Send notification for absent/late status
            if attendance_data.status in [AttendanceStatus.ABSENT, AttendanceStatus.LATE]:
                person_name = student.full_name if student else teacher.full_name
                person_email = student.user.email if student else teacher.user.email
                
                if attendance_data.status == AttendanceStatus.ABSENT:
                    NotificationService.send_attendance_alert(
                        person_email, person_name, "absent", attendance_data.date, tenant_id
                    )
                elif attendance_data.status == AttendanceStatus.LATE:
                    NotificationService.send_attendance_alert(
                        person_email, person_name, "late", attendance_data.date, tenant_id
                    )
            
            logger.info(f"Marked attendance for {person_type} {person_id} on {attendance_data.date}")
            return attendance_record
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking attendance: {str(e)}")
            raise
    
    @staticmethod
    def mark_attendance_by_qr(
        db: Session,
        qr_code: str,
        tenant_id: int,
        user_id: int,
        location: Optional[str] = None
    ) -> AttendanceRecord:
        """Mark attendance using QR code"""
        try:
            # Verify QR code
            qr_record = db.query(QRCode).filter(
                and_(
                    QRCode.code == qr_code,
                    QRCode.tenant_id == tenant_id,
                    QRCode.is_active == True
                )
            ).first()
            
            if not qr_record:
                raise ValueError("Invalid QR code")
            
            if not qr_record.is_valid():
                raise ValueError("QR code has expired")
            
            if not qr_record.can_be_used():
                raise ValueError("QR code usage limit exceeded")
            
            # Get current user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            
            # Determine if user is student or teacher
            student = db.query(Student).filter(
                and_(Student.user_id == user_id, Student.tenant_id == tenant_id)
            ).first()
            
            teacher = db.query(Teacher).filter(
                and_(Teacher.user_id == user_id, Teacher.tenant_id == tenant_id)
            ).first()
            
            if not student and not teacher:
                raise ValueError("User is not a student or teacher")
            
            # Create attendance data
            attendance_data = AttendanceMarkRequest(
                student_id=student.id if student else None,
                teacher_id=teacher.id if teacher else None,
                date=date.today(),
                status=AttendanceStatus.PRESENT,
                method=AttendanceMethod.QR_SCANNER,
                location=location,
                notes=f"Marked via QR code: {qr_code}"
            )
            
            # Mark attendance
            attendance_record = AttendanceService.mark_attendance(
                db, attendance_data, tenant_id, user_id
            )
            
            # Increment QR code usage
            qr_record.increment_usage()
            db.commit()
            
            return attendance_record
            
        except Exception as e:
            logger.error(f"Error marking attendance by QR: {str(e)}")
            raise
    
    @staticmethod
    def mark_attendance_by_geolocation(
        db: Session,
        latitude: float,
        longitude: float,
        tenant_id: int,
        user_id: int,
        allowed_radius: float = 100  # meters
    ) -> AttendanceRecord:
        """Mark attendance using geolocation"""
        try:
            # Get current user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            
            # Determine if user is student or teacher
            student = db.query(Student).filter(
                and_(Student.user_id == user_id, Student.tenant_id == tenant_id)
            ).first()
            
            teacher = db.query(Teacher).filter(
                and_(Teacher.user_id == user_id, Teacher.tenant_id == tenant_id)
            ).first()
            
            if not student and not teacher:
                raise ValueError("User is not a student or teacher")
            
            # Get school location from tenant settings
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant or not tenant.school_latitude or not tenant.school_longitude:
                raise ValueError("School location not configured")
            
            # Calculate distance from school
            school_location = (tenant.school_latitude, tenant.school_longitude)
            user_location = (latitude, longitude)
            distance = geodesic(school_location, user_location).meters
            
            if distance > allowed_radius:
                raise ValueError(f"Location too far from school. Distance: {distance:.0f}m, Allowed: {allowed_radius}m")
            
            # Create attendance data
            attendance_data = AttendanceMarkRequest(
                student_id=student.id if student else None,
                teacher_id=teacher.id if teacher else None,
                date=date.today(),
                status=AttendanceStatus.PRESENT,
                method=AttendanceMethod.GEOLOCATION,
                location=f"Lat: {latitude}, Long: {longitude}, Distance: {distance:.0f}m"
            )
            
            # Mark attendance
            attendance_record = AttendanceService.mark_attendance(
                db, attendance_data, tenant_id, user_id
            )
            
            return attendance_record
            
        except Exception as e:
            logger.error(f"Error marking attendance by geolocation: {str(e)}")
            raise
    
    @staticmethod
    def get_attendance_records(
        db: Session,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        search: Optional[AttendanceSearch] = None
    ) -> AttendanceList:
        """Get paginated attendance records with optional filtering"""
        try:
            query = db.query(AttendanceRecord).filter(AttendanceRecord.tenant_id == tenant_id)
            
            # Apply search filters
            if search:
                if search.student_id:
                    query = query.filter(AttendanceRecord.student_id == search.student_id)
                
                if search.teacher_id:
                    query = query.filter(AttendanceRecord.teacher_id == search.teacher_id)
                
                if search.date_from:
                    query = query.filter(AttendanceRecord.date >= search.date_from)
                
                if search.date_to:
                    query = query.filter(AttendanceRecord.date <= search.date_to)
                
                if search.status:
                    query = query.filter(AttendanceRecord.status == search.status)
                
                if search.method:
                    query = query.filter(AttendanceRecord.method == search.method)
            
            # Get total count
            total = query.count()
            
            # Apply pagination and ordering
            records = query.order_by(desc(AttendanceRecord.date), desc(AttendanceRecord.created_at)).offset(skip).limit(limit).all()
            
            return AttendanceList(
                records=records,
                total=total,
                skip=skip,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error getting attendance records: {str(e)}")
            raise
    
    @staticmethod
    def get_attendance_stats(
        db: Session,
        tenant_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        student_id: Optional[int] = None,
        teacher_id: Optional[int] = None
    ) -> AttendanceStats:
        """Get attendance statistics"""
        try:
            query = db.query(AttendanceRecord).filter(AttendanceRecord.tenant_id == tenant_id)
            
            if start_date:
                query = query.filter(AttendanceRecord.date >= start_date)
            
            if end_date:
                query = query.filter(AttendanceRecord.date <= end_date)
            
            if student_id:
                query = query.filter(AttendanceRecord.student_id == student_id)
            
            if teacher_id:
                query = query.filter(AttendanceRecord.teacher_id == teacher_id)
            
            # Get total records
            total_records = query.count()
            
            # Get status counts
            present_count = query.filter(AttendanceRecord.status == AttendanceStatus.PRESENT).count()
            absent_count = query.filter(AttendanceRecord.status == AttendanceStatus.ABSENT).count()
            late_count = query.filter(AttendanceRecord.status == AttendanceStatus.LATE).count()
            leave_count = query.filter(AttendanceRecord.status == AttendanceStatus.LEAVE).count()
            
            # Calculate percentages
            total = present_count + absent_count + late_count + leave_count
            present_percentage = (present_count / total * 100) if total > 0 else 0
            absent_percentage = (absent_count / total * 100) if total > 0 else 0
            late_percentage = (late_count / total * 100) if total > 0 else 0
            leave_percentage = (leave_count / total * 100) if total > 0 else 0
            
            return AttendanceStats(
                total_records=total_records,
                present_count=present_count,
                absent_count=absent_count,
                late_count=late_count,
                leave_count=leave_count,
                present_percentage=round(present_percentage, 2),
                absent_percentage=round(absent_percentage, 2),
                late_percentage=round(late_percentage, 2),
                leave_percentage=round(leave_percentage, 2)
            )
            
        except Exception as e:
            logger.error(f"Error getting attendance stats: {str(e)}")
            raise
    
    @staticmethod
    def generate_qr_code(
        db: Session,
        qr_data: QRCodeCreate,
        tenant_id: int
    ) -> QRCodeResponse:
        """Generate a new QR code for attendance"""
        try:
            # Create QR code record
            qr_record = QRCode(
                tenant_id=tenant_id,
                code=qr_data.code,
                description=qr_data.description,
                valid_from=qr_data.valid_from,
                valid_until=qr_data.valid_until,
                max_usage=qr_data.max_usage,
                location=qr_data.location,
                created_by=qr_data.created_by
            )
            
            db.add(qr_record)
            db.commit()
            db.refresh(qr_record)
            
            # Generate QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data.code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return QRCodeResponse(
                id=qr_record.id,
                code=qr_record.code,
                description=qr_record.description,
                valid_from=qr_record.valid_from,
                valid_until=qr_record.valid_until,
                max_usage=qr_record.max_usage,
                current_usage=qr_record.current_usage,
                location=qr_record.location,
                is_active=qr_record.is_active,
                created_at=qr_record.created_at,
                qr_image=f"data:image/png;base64,{img_str}"
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating QR code: {str(e)}")
            raise
    
    @staticmethod
    def verify_qr_code(db: Session, qr_code: str, tenant_id: int) -> bool:
        """Verify if a QR code is valid"""
        try:
            qr_record = db.query(QRCode).filter(
                and_(
                    QRCode.code == qr_code,
                    QRCode.tenant_id == tenant_id,
                    QRCode.is_active == True
                )
            ).first()
            
            if not qr_record:
                return False
            
            return qr_record.is_valid() and qr_record.can_be_used()
            
        except Exception as e:
            logger.error(f"Error verifying QR code: {str(e)}")
            return False
    
    @staticmethod
    def _update_student_attendance_percentage(db: Session, student_id: int, tenant_id: int):
        """Update student's attendance percentage"""
        try:
            from datetime import date, timedelta
            
            # Get attendance records for the last 30 days
            thirty_days_ago = date.today() - timedelta(days=30)
            
            total_days = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.student_id == student_id,
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= thirty_days_ago
                )
            ).count()
            
            present_days = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.student_id == student_id,
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= thirty_days_ago,
                    AttendanceRecord.status == AttendanceStatus.PRESENT
                )
            ).count()
            
            attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
            
            # Update student record
            student = db.query(Student).filter(Student.id == student_id).first()
            if student:
                student.attendance_percentage = round(attendance_percentage, 2)
                db.commit()
                
        except Exception as e:
            logger.error(f"Error updating student attendance percentage: {str(e)}")
    
    @staticmethod
    def _update_teacher_attendance_percentage(db: Session, teacher_id: int, tenant_id: int):
        """Update teacher's attendance percentage"""
        try:
            from datetime import date, timedelta
            
            # Get attendance records for the last 30 days
            thirty_days_ago = date.today() - timedelta(days=30)
            
            total_days = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.teacher_id == teacher_id,
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= thirty_days_ago
                )
            ).count()
            
            present_days = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.teacher_id == teacher_id,
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.date >= thirty_days_ago,
                    AttendanceRecord.status == AttendanceStatus.PRESENT
                )
            ).count()
            
            attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
            
            # Update teacher record
            teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
            if teacher:
                teacher.attendance_percentage = round(attendance_percentage, 2)
                db.commit()
                
        except Exception as e:
            logger.error(f"Error updating teacher attendance percentage: {str(e)}")