"""Hostel API endpoints"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, RoleChecker
from app.models.user import User
router = APIRouter()

@router.get("/")
async def get_hostel_info(current_user: User = Depends(get_current_user)):
    return {"message": "Hostel API - Coming soon"}

@router.post("/")
async def create_hostel_record(current_user: User = Depends(RoleChecker.require_admin())):
    return {"message": "Create hostel record - Coming soon"}