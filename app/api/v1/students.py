"""
Students API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.models.user import User, UserRole
from app.models.student import Student, StudentStatus, StudentGrade
from app.models.tenant import Tenant
from app.schemas.student import (
    StudentCreate, StudentUpdate, StudentResponse, StudentList,
    StudentSearch, StudentStats
)
from app.services.student_service import StudentService

router = APIRouter()


@router.post("/", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    current_user: User = Depends(RoleChecker.require_admin()),
    db: Session = Depends(get_db)
):
    """Create a new student"""
    try:
        student = await StudentService.create_student(db, student_data, current_user.tenant_id)
        return StudentResponse.from_orm(student)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=StudentList)
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    grade: Optional[StudentGrade] = None,
    status: Optional[StudentStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of students with filtering and pagination"""
    try:
        students, total = await StudentService.get_students(
            db, current_user.tenant_id, skip, limit, search, grade, status
        )
        return StudentList(
            students=[StudentResponse.from_orm(student) for student in students],
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student by ID"""
    try:
        student = await StudentService.get_student(db, student_id, current_user.tenant_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return StudentResponse.from_orm(student)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: str,
    student_data: StudentUpdate,
    current_user: User = Depends(RoleChecker.require_admin()),
    db: Session = Depends(get_db)
):
    """Update student information"""
    try:
        student = await StudentService.update_student(db, student_id, student_data, current_user.tenant_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return StudentResponse.from_orm(student)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{student_id}")
async def delete_student(
    student_id: str,
    current_user: User = Depends(RoleChecker.require_admin()),
    db: Session = Depends(get_db)
):
    """Delete student (soft delete)"""
    try:
        success = await StudentService.delete_student(db, student_id, current_user.tenant_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return {"message": "Student deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{student_id}/profile", response_model=StudentResponse)
async def get_student_profile(
    student_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student profile (for students to view their own profile)"""
    try:
        # Students can only view their own profile
        if current_user.role == UserRole.STUDENT:
            student = db.query(Student).filter(
                Student.user_id == current_user.id,
                Student.tenant_id == current_user.tenant_id
            ).first()
            if not student or student.id != student_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        student = await StudentService.get_student(db, student_id, current_user.tenant_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return StudentResponse.from_orm(student)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{student_id}/attendance")
async def get_student_attendance(
    student_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student attendance records"""
    try:
        # Students can only view their own attendance
        if current_user.role == UserRole.STUDENT:
            student = db.query(Student).filter(
                Student.user_id == current_user.id,
                Student.tenant_id == current_user.tenant_id
            ).first()
            if not student or student.id != student_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        attendance_records = await StudentService.get_student_attendance(
            db, student_id, current_user.tenant_id, start_date, end_date
        )
        return {"attendance_records": attendance_records}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{student_id}/grades")
async def get_student_grades(
    student_id: str,
    academic_year: Optional[str] = None,
    semester: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student grades"""
    try:
        # Students can only view their own grades
        if current_user.role == UserRole.STUDENT:
            student = db.query(Student).filter(
                Student.user_id == current_user.id,
                Student.tenant_id == current_user.tenant_id
            ).first()
            if not student or student.id != student_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        grades = await StudentService.get_student_grades(
            db, student_id, current_user.tenant_id, academic_year, semester
        )
        return {"grades": grades}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{student_id}/fees")
async def get_student_fees(
    student_id: str,
    fee_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student fee records"""
    try:
        # Students can only view their own fees
        if current_user.role == UserRole.STUDENT:
            student = db.query(Student).filter(
                Student.user_id == current_user.id,
                Student.tenant_id == current_user.tenant_id
            ).first()
            if not student or student.id != student_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        fees = await StudentService.get_student_fees(
            db, student_id, current_user.tenant_id, fee_type, status
        )
        return {"fees": fees}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats/overview", response_model=StudentStats)
async def get_student_stats(
    current_user: User = Depends(RoleChecker.require_admin()),
    db: Session = Depends(get_db)
):
    """Get student statistics overview"""
    try:
        stats = await StudentService.get_student_stats(db, current_user.tenant_id)
        return StudentStats(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/bulk-import")
async def bulk_import_students(
    file_upload,
    current_user: User = Depends(RoleChecker.require_admin()),
    db: Session = Depends(get_db)
):
    """Bulk import students from CSV/Excel file"""
    try:
        result = await StudentService.bulk_import_students(
            db, file_upload, current_user.tenant_id
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/export/csv")
async def export_students_csv(
    current_user: User = Depends(RoleChecker.require_admin()),
    db: Session = Depends(get_db)
):
    """Export students data to CSV"""
    try:
        csv_data = await StudentService.export_students_csv(db, current_user.tenant_id)
        return {"csv_data": csv_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )