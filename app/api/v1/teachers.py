"""
Teachers API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.models.user import User

router = APIRouter()


@router.get("/")
async def get_teachers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of teachers"""
    return {"message": "Teachers API - Coming soon"}


@router.post("/")
async def create_teacher(current_user: User = Depends(RoleChecker.require_admin()), db: Session = Depends(get_db)):
    """Create a new teacher"""
    return {"message": "Create teacher - Coming soon"}


@router.get("/{teacher_id}")
async def get_teacher(teacher_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get teacher by ID"""
    return {"message": f"Get teacher {teacher_id} - Coming soon"}


@router.put("/{teacher_id}")
async def update_teacher(teacher_id: str, current_user: User = Depends(RoleChecker.require_admin()), db: Session = Depends(get_db)):
    """Update teacher information"""
    return {"message": f"Update teacher {teacher_id} - Coming soon"}


@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: str, current_user: User = Depends(RoleChecker.require_admin()), db: Session = Depends(get_db)):
    """Delete teacher"""
    return {"message": f"Delete teacher {teacher_id} - Coming soon"}