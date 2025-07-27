"""
Attendance API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.models.user import User

router = APIRouter()


@router.post("/mark")
async def mark_attendance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark attendance"""
    return {"message": "Mark attendance - Coming soon"}


@router.get("/")
async def get_attendance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get attendance records"""
    return {"message": "Get attendance - Coming soon"}


@router.post("/qr-generate")
async def generate_qr_code(current_user: User = Depends(RoleChecker.require_teacher()), db: Session = Depends(get_db)):
    """Generate QR code for attendance"""
    return {"message": "Generate QR code - Coming soon"}


@router.post("/qr-scan")
async def scan_qr_code(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Scan QR code for attendance"""
    return {"message": "Scan QR code - Coming soon"}


@router.post("/geolocation")
async def mark_attendance_geolocation(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark attendance using geolocation"""
    return {"message": "Geolocation attendance - Coming soon"}