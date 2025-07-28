from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date
import logging

from app.models.teacher import Teacher, TeacherStatus, TeacherQualification
from app.models.user import User, UserRole, UserStatus
from app.models.tenant import Tenant
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse, TeacherList, TeacherSearch
from app.services.auth_service import AuthService
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class TeacherService:
    """Service class for teacher management operations"""
    
    @staticmethod
    def create_teacher(db: Session, teacher_data: TeacherCreate, tenant_id: int) -> Teacher:
        """Create a new teacher with associated user account"""
        try:
            # Create user account for teacher
            user_data = {
                "email": teacher_data.email,
                "username": teacher_data.username,
                "password": teacher_data.password,
                "first_name": teacher_data.first_name,
                "last_name": teacher_data.last_name,
                "role": UserRole.TEACHER,
                "tenant_id": tenant_id,
                "is_email_verified": True  # Teachers are pre-verified
            }
            
            user = AuthService.create_user(db, user_data)
            
            # Create teacher profile
            teacher = Teacher(
                user_id=user.id,
                tenant_id=tenant_id,
                employee_id=teacher_data.employee_id,
                date_of_birth=teacher_data.date_of_birth,
                gender=teacher_data.gender,
                phone=teacher_data.phone,
                address=teacher_data.address,
                city=teacher_data.city,
                state=teacher_data.state,
                country=teacher_data.country,
                postal_code=teacher_data.postal_code,
                qualification=teacher_data.qualification,
                specialization=teacher_data.specialization,
                hire_date=teacher_data.hire_date,
                salary=teacher_data.salary,
                status=TeacherStatus.ACTIVE,
                emergency_contact_name=teacher_data.emergency_contact_name,
                emergency_contact_phone=teacher_data.emergency_contact_phone,
                emergency_contact_relationship=teacher_data.emergency_contact_relationship,
                medical_conditions=teacher_data.medical_conditions,
                allergies=teacher_data.allergies,
                blood_group=teacher_data.blood_group,
                transport_required=teacher_data.transport_required,
                transport_route=teacher_data.transport_route,
                hostel_required=teacher_data.hostel_required,
                hostel_room=teacher_data.hostel_room,
                experience_years=teacher_data.experience_years,
                experience_details=teacher_data.experience_details,
                certificates=teacher_data.certificates,
                bio=teacher_data.bio,
                profile_picture=teacher_data.profile_picture
            )
            
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            
            # Send welcome notification
            NotificationService.send_welcome_email(
                user.email, 
                user.first_name, 
                "teacher",
                tenant_id
            )
            
            logger.info(f"Created teacher {teacher.id} for tenant {tenant_id}")
            return teacher
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating teacher: {str(e)}")
            raise
    
    @staticmethod
    def get_teachers(
        db: Session, 
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        search: Optional[TeacherSearch] = None
    ) -> TeacherList:
        """Get paginated list of teachers with optional filtering"""
        try:
            query = db.query(Teacher).filter(Teacher.tenant_id == tenant_id)
            
            # Apply search filters
            if search:
                if search.name:
                    query = query.join(User).filter(
                        or_(
                            func.lower(User.first_name).contains(search.name.lower()),
                            func.lower(User.last_name).contains(search.name.lower()),
                            func.lower(User.first_name + ' ' + User.last_name).contains(search.name.lower())
                        )
                    )
                
                if search.status:
                    query = query.filter(Teacher.status == search.status)
                
                if search.qualification:
                    query = query.filter(Teacher.qualification == search.qualification)
                
                if search.specialization:
                    query = query.filter(Teacher.specialization.contains(search.specialization))
                
                if search.employee_id:
                    query = query.filter(Teacher.employee_id.contains(search.employee_id))
                
                if search.hire_date_from:
                    query = query.filter(Teacher.hire_date >= search.hire_date_from)
                
                if search.hire_date_to:
                    query = query.filter(Teacher.hire_date <= search.hire_date_to)
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            teachers = query.offset(skip).limit(limit).all()
            
            return TeacherList(
                teachers=teachers,
                total=total,
                skip=skip,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error getting teachers: {str(e)}")
            raise
    
    @staticmethod
    def get_teacher(db: Session, teacher_id: int, tenant_id: int) -> Optional[Teacher]:
        """Get a specific teacher by ID"""
        try:
            return db.query(Teacher).filter(
                and_(Teacher.id == teacher_id, Teacher.tenant_id == tenant_id)
            ).first()
        except Exception as e:
            logger.error(f"Error getting teacher {teacher_id}: {str(e)}")
            raise
    
    @staticmethod
    def update_teacher(
        db: Session, 
        teacher_id: int, 
        teacher_data: TeacherUpdate, 
        tenant_id: int
    ) -> Optional[Teacher]:
        """Update teacher information"""
        try:
            teacher = TeacherService.get_teacher(db, teacher_id, tenant_id)
            if not teacher:
                return None
            
            # Update teacher fields
            update_data = teacher_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(teacher, field, value)
            
            # Update associated user if provided
            if teacher_data.user_update:
                user = teacher.user
                user_update_data = teacher_data.user_update.dict(exclude_unset=True)
                for field, value in user_update_data.items():
                    setattr(user, field, value)
            
            teacher.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(teacher)
            
            logger.info(f"Updated teacher {teacher_id}")
            return teacher
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating teacher {teacher_id}: {str(e)}")
            raise
    
    @staticmethod
    def delete_teacher(db: Session, teacher_id: int, tenant_id: int) -> bool:
        """Soft delete a teacher"""
        try:
            teacher = TeacherService.get_teacher(db, teacher_id, tenant_id)
            if not teacher:
                return False
            
            # Soft delete teacher
            teacher.status = TeacherStatus.INACTIVE
            teacher.deleted_at = datetime.utcnow()
            
            # Soft delete associated user
            if teacher.user:
                teacher.user.status = UserStatus.INACTIVE
                teacher.user.deleted_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"Deleted teacher {teacher_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting teacher {teacher_id}: {str(e)}")
            raise
    
    @staticmethod
    def get_teacher_attendance(
        db: Session, 
        teacher_id: int, 
        tenant_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get teacher attendance records"""
        try:
            from app.models.attendance import AttendanceRecord
            
            query = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.teacher_id == teacher_id,
                    AttendanceRecord.tenant_id == tenant_id
                )
            )
            
            if start_date:
                query = query.filter(AttendanceRecord.date >= start_date)
            
            if end_date:
                query = query.filter(AttendanceRecord.date <= end_date)
            
            records = query.order_by(AttendanceRecord.date.desc()).all()
            
            return [
                {
                    "id": record.id,
                    "date": record.date,
                    "status": record.status,
                    "method": record.method,
                    "check_in_time": record.check_in_time,
                    "check_out_time": record.check_out_time,
                    "location": record.location,
                    "notes": record.notes
                }
                for record in records
            ]
            
        except Exception as e:
            logger.error(f"Error getting teacher attendance: {str(e)}")
            raise
    
    @staticmethod
    def get_teacher_stats(db: Session, teacher_id: int, tenant_id: int) -> Dict[str, Any]:
        """Get teacher statistics and performance metrics"""
        try:
            teacher = TeacherService.get_teacher(teacher_id, tenant_id)
            if not teacher:
                return {}
            
            # Calculate attendance percentage
            from app.models.attendance import AttendanceRecord
            total_days = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.teacher_id == teacher_id,
                    AttendanceRecord.tenant_id == tenant_id
                )
            ).count()
            
            present_days = db.query(AttendanceRecord).filter(
                and_(
                    AttendanceRecord.teacher_id == teacher_id,
                    AttendanceRecord.tenant_id == tenant_id,
                    AttendanceRecord.status == "present"
                )
            ).count()
            
            attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
            
            # Calculate experience
            experience_years = teacher.experience_years or 0
            if teacher.hire_date:
                from datetime import date
                today = date.today()
                experience_years = (today - teacher.hire_date).days / 365.25
            
            return {
                "teacher_id": teacher_id,
                "full_name": teacher.full_name,
                "employee_id": teacher.employee_id,
                "qualification": teacher.qualification_display,
                "specialization": teacher.specialization,
                "hire_date": teacher.hire_date,
                "experience_years": round(experience_years, 1),
                "attendance_percentage": round(attendance_percentage, 2),
                "total_attendance_days": total_days,
                "present_days": present_days,
                "status": teacher.status,
                "salary": teacher.salary,
                "emergency_contacts": teacher.get_emergency_contacts(),
                "certificates": teacher.get_certificates(),
                "experience_details": teacher.get_experience_details()
            }
            
        except Exception as e:
            logger.error(f"Error getting teacher stats: {str(e)}")
            raise
    
    @staticmethod
    def bulk_import_teachers(
        db: Session, 
        teachers_data: List[TeacherCreate], 
        tenant_id: int
    ) -> Dict[str, Any]:
        """Bulk import teachers from CSV or other sources"""
        try:
            results = {
                "total": len(teachers_data),
                "successful": 0,
                "failed": 0,
                "errors": []
            }
            
            for i, teacher_data in enumerate(teachers_data):
                try:
                    TeacherService.create_teacher(db, teacher_data, tenant_id)
                    results["successful"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({
                        "row": i + 1,
                        "error": str(e),
                        "data": teacher_data.dict()
                    })
            
            logger.info(f"Bulk import completed: {results['successful']} successful, {results['failed']} failed")
            return results
            
        except Exception as e:
            logger.error(f"Error in bulk import: {str(e)}")
            raise
    
    @staticmethod
    def export_teachers_csv(db: Session, tenant_id: int) -> str:
        """Export teachers data to CSV format"""
        try:
            import csv
            import io
            
            teachers = db.query(Teacher).filter(Teacher.tenant_id == tenant_id).all()
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                "Employee ID", "First Name", "Last Name", "Email", "Phone",
                "Qualification", "Specialization", "Hire Date", "Salary",
                "Status", "Address", "City", "State", "Country"
            ])
            
            # Write data
            for teacher in teachers:
                writer.writerow([
                    teacher.employee_id,
                    teacher.user.first_name if teacher.user else "",
                    teacher.user.last_name if teacher.user else "",
                    teacher.user.email if teacher.user else "",
                    teacher.phone,
                    teacher.qualification_display,
                    teacher.specialization,
                    teacher.hire_date,
                    teacher.salary,
                    teacher.status,
                    teacher.address,
                    teacher.city,
                    teacher.state,
                    teacher.country
                ])
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error exporting teachers CSV: {str(e)}")
            raise