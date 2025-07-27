"""LMS API endpoints"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, RoleChecker
from app.models.user import User
router = APIRouter()

@router.get("/courses")
async def get_courses(current_user: User = Depends(get_current_user)):
    return {"message": "LMS Courses API - Coming soon"}

@router.get("/assignments")
async def get_assignments(current_user: User = Depends(get_current_user)):
    return {"message": "LMS Assignments API - Coming soon"}

@router.get("/grades")
async def get_grades(current_user: User = Depends(get_current_user)):
    return {"message": "LMS Grades API - Coming soon"}