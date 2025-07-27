"""Tenants API endpoints"""
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, RoleChecker
from app.models.user import User
router = APIRouter()

@router.get("/")
async def get_tenants(current_user: User = Depends(RoleChecker.require_super_admin())):
    return {"message": "Tenants API - Coming soon"}

@router.post("/")
async def create_tenant(current_user: User = Depends(RoleChecker.require_super_admin())):
    return {"message": "Create tenant - Coming soon"}

@router.get("/{tenant_id}")
async def get_tenant(tenant_id: str, current_user: User = Depends(RoleChecker.require_super_admin())):
    return {"message": f"Get tenant {tenant_id} - Coming soon"}