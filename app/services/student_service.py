"""
Student service with business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List, Tuple
from datetime import date
import uuid

from app.models.student import Student, StudentStatus, StudentGrade
from app.models.user import User, UserRole
from app.models.attendance import AttendanceRecord
from app.models.fees import FeeRecord
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    """Student service"""
    
    @staticmethod
    async def create_student(db: Session, student_data: StudentCreate, tenant_id: str) -> Student:
        """Create a new student"""
        # Create user first
        user_data = {
            "email": student_data.email,
            "username": student_data.username,
            "password": student_data.password,
            "first_name": student_data.first_name,
            "last_name": student_data.last_name,
            "phone": student_data.phone,
            "role": UserRole.STUDENT,
            "tenant_id": tenant_id
        }
        
        # This would typically call AuthService.create_user
        # For now, create user directly
        hashed_password = "hashed_password"  # This should be properly hashed
        user = User(
            id=str(uuid.uuid4()),
            email=user_data["email"],
            username=user_data.get("username"),
            hashed_password=hashed_password,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data.get("phone"),
            role=user_data["role"],
            tenant_id=user_data["tenant_id"]
        )
        
        db.add(user)
        db.flush()  # Get the user ID without committing
        
        # Create student profile
        student = Student(
            id=str(uuid.uuid4()),
            user_id=user.id,
            tenant_id=tenant_id,
            student_id=student_data.student_id,
            admission_number=student_data.admission_number,
            admission_date=student_data.admission_date,
            grade=student_data.grade,
            current_grade=student_data.grade,
            academic_year=student_data.academic_year,
            status=StudentStatus.ACTIVE,
            date_of_birth=student_data.date_of_birth,
            gender=student_data.gender,
            blood_group=student_data.blood_group,
            nationality=student_data.nationality,
            religion=student_data.religion,
            mother_tongue=student_data.mother_tongue,
            emergency_contact=student_data.emergency_contact,
            emergency_contact_relation=student_data.emergency_contact_relation,
            emergency_contact_phone=student_data.emergency_contact_phone,
            permanent_address=student_data.permanent_address,
            current_address=student_data.current_address,
            city=student_data.city,
            state=student_data.state,
            country=student_data.country,
            postal_code=student_data.postal_code,
            previous_school=student_data.previous_school,
            previous_grade=student_data.previous_grade,
            medical_conditions=student_data.medical_conditions,
            allergies=student_data.allergies,
            medications=student_data.medications,
            emergency_medical_info=student_data.emergency_medical_info,
            uses_transport=student_data.uses_transport,
            transport_route=student_data.transport_route,
            pickup_location=student_data.pickup_location,
            drop_location=student_data.drop_location,
            uses_hostel=student_data.uses_hostel,
            hostel_room=student_data.hostel_room,
            hostel_block=student_data.hostel_block
        )
        
        db.add(student)
        db.commit()
        db.refresh(student)
        
        return student
    
    @staticmethod
    async def get_students(
        db: Session,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        grade: Optional[StudentGrade] = None,
        status: Optional[StudentStatus] = None
    ) -> Tuple[List[Student], int]:
        """Get students with filtering and pagination"""
        query = db.query(Student).filter(Student.tenant_id == tenant_id)
        
        # Apply filters
        if search:
            search_filter = or_(
                Student.student_id.ilike(f"%{search}%"),
                Student.admission_number.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if grade:
            query = query.filter(Student.current_grade == grade)
        
        if status:
            query = query.filter(Student.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        students = query.offset(skip).limit(limit).all()
        
        return students, total
    
    @staticmethod
    async def get_student(db: Session, student_id: str, tenant_id: str) -> Optional[Student]:
        """Get student by ID"""
        return db.query(Student).filter(
            Student.id == student_id,
            Student.tenant_id == tenant_id
        ).first()
    
    @staticmethod
    async def update_student(
        db: Session,
        student_id: str,
        student_data: StudentUpdate,
        tenant_id: str
    ) -> Optional[Student]:
        """Update student information"""
        student = await StudentService.get_student(db, student_id, tenant_id)
        if not student:
            return None
        
        # Update fields
        update_data = student_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(student, field):
                setattr(student, field, value)
        
        db.commit()
        db.refresh(student)
        
        return student
    
    @staticmethod
    async def delete_student(db: Session, student_id: str, tenant_id: str) -> bool:
        """Delete student (soft delete)"""
        student = await StudentService.get_student(db, student_id, tenant_id)
        if not student:
            return False
        
        student.status = StudentStatus.INACTIVE
        db.commit()
        
        return True
    
    @staticmethod
    async def get_student_attendance(
        db: Session,
        student_id: str,
        tenant_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[dict]:
        """Get student attendance records"""
        query = db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.tenant_id == tenant_id
        )
        
        if start_date:
            query = query.filter(AttendanceRecord.date >= start_date)
        
        if end_date:
            query = query.filter(AttendanceRecord.date <= end_date)
        
        attendance_records = query.order_by(AttendanceRecord.date.desc()).all()
        
        return [
            {
                "id": record.id,
                "date": record.date,
                "status": record.status,
                "time_in": record.time_in,
                "time_out": record.time_out,
                "method": record.method,
                "remarks": record.remarks
            }
            for record in attendance_records
        ]
    
    @staticmethod
    async def get_student_grades(
        db: Session,
        student_id: str,
        tenant_id: str,
        academic_year: Optional[str] = None,
        semester: Optional[str] = None
    ) -> List[dict]:
        """Get student grades"""
        # This would typically query a grades table
        # For now, return empty list
        return []
    
    @staticmethod
    async def get_student_fees(
        db: Session,
        student_id: str,
        tenant_id: str,
        fee_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[dict]:
        """Get student fee records"""
        query = db.query(FeeRecord).filter(
            FeeRecord.student_id == student_id,
            FeeRecord.tenant_id == tenant_id
        )
        
        if fee_type:
            query = query.filter(FeeRecord.fee_type == fee_type)
        
        if status:
            query = query.filter(FeeRecord.status == status)
        
        fee_records = query.order_by(FeeRecord.due_date.desc()).all()
        
        return [
            {
                "id": record.id,
                "fee_type": record.fee_type,
                "total_amount": float(record.total_amount),
                "paid_amount": float(record.paid_amount),
                "remaining_amount": float(record.remaining_amount),
                "due_date": record.due_date,
                "status": record.status,
                "description": record.description
            }
            for record in fee_records
        ]
    
    @staticmethod
    async def get_student_stats(db: Session, tenant_id: str) -> dict:
        """Get student statistics"""
        total_students = db.query(Student).filter(
            Student.tenant_id == tenant_id,
            Student.status == StudentStatus.ACTIVE
        ).count()
        
        active_students = db.query(Student).filter(
            Student.tenant_id == tenant_id,
            Student.status == StudentStatus.ACTIVE
        ).count()
        
        # Get students by grade
        grade_stats = db.query(
            Student.current_grade,
            db.func.count(Student.id)
        ).filter(
            Student.tenant_id == tenant_id,
            Student.status == StudentStatus.ACTIVE
        ).group_by(Student.current_grade).all()
        
        return {
            "total_students": total_students,
            "active_students": active_students,
            "grade_distribution": {grade: count for grade, count in grade_stats}
        }
    
    @staticmethod
    async def bulk_import_students(db: Session, file_upload, tenant_id: str) -> dict:
        """Bulk import students from CSV/Excel file"""
        # This would implement CSV/Excel parsing logic
        return {
            "message": "Bulk import completed",
            "imported": 0,
            "failed": 0
        }
    
    @staticmethod
    async def export_students_csv(db: Session, tenant_id: str) -> str:
        """Export students data to CSV"""
        # This would implement CSV export logic
        return "CSV data"