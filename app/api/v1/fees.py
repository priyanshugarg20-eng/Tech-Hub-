"""
Fees API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.models.user import User

router = APIRouter()


@router.get("/")
async def get_fees(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get fee records"""
    return {"message": "Get fees - Coming soon"}


@router.post("/")
async def create_fee(current_user: User = Depends(RoleChecker.require_admin()), db: Session = Depends(get_db)):
    """Create fee record"""
    return {"message": "Create fee - Coming soon"}


@router.post("/payment")
async def record_payment(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Record payment"""
    return {"message": "Record payment - Coming soon"}


@router.get("/reports")
async def get_fee_reports(current_user: User = Depends(RoleChecker.require_admin()), db: Session = Depends(get_db)):
    """Get fee reports"""
    return {"message": "Fee reports - Coming soon"}


@router.post("/reminders")
async def send_fee_reminders(current_user: User = Depends(RoleChecker.require_admin()), db: Session = Depends(get_db)):
    """Send fee reminders"""
    return {"message": "Send reminders - Coming soon"}