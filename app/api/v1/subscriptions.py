"""Subscriptions API endpoints"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, RoleChecker
from app.models.user import User
router = APIRouter()

@router.get("/plans")
async def get_subscription_plans(current_user: User = Depends(get_current_user)):
    return {"message": "Subscription plans - Coming soon"}

@router.post("/subscribe")
async def subscribe(current_user: User = Depends(RoleChecker.require_admin())):
    return {"message": "Subscribe - Coming soon"}

@router.get("/billing")
async def get_billing_info(current_user: User = Depends(RoleChecker.require_admin())):
    return {"message": "Billing info - Coming soon"}