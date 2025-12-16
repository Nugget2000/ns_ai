
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..services.user_service import UserService
from ..models.schemas import UserResponse, UserUpdate, UserRole
from ..core.auth import get_admin_user, get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current user profile.
    """
    return current_user

@router.get("/", response_model=List[UserResponse])
async def list_users(current_admin: UserResponse = Depends(get_admin_user)):
    """
    List all users (Admin only).
    """
    return UserService.list_users()

@router.put("/{uid}/role", response_model=UserResponse)
async def update_user_role(
    uid: str, 
    role_update: UserUpdate, 
    current_admin: UserResponse = Depends(get_admin_user)
):
    """
    Update user role (Admin only).
    """
    updated_user = UserService.update_user(uid, role_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
