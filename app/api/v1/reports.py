"""Reports API endpoints"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, RoleChecker
from app.models.user import User
router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(current_user: User = Depends(get_current_user)):
    return {"message": "Dashboard reports - Coming soon"}

@router.get("/attendance")
async def get_attendance_reports(current_user: User = Depends(RoleChecker.require_admin())):
    return {"message": "Attendance reports - Coming soon"}

@router.get("/academic")
async def get_academic_reports(current_user: User = Depends(get_current_user)):
    return {"message": "Academic reports - Coming soon"}