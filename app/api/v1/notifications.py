"""Notifications API endpoints"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, RoleChecker
from app.models.user import User
router = APIRouter()

@router.get("/")
async def get_notifications(current_user: User = Depends(get_current_user)):
    return {"message": "Notifications API - Coming soon"}

@router.post("/send")
async def send_notification(current_user: User = Depends(RoleChecker.require_admin())):
    return {"message": "Send notification - Coming soon"}