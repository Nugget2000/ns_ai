"""
Admin API endpoints for user activity monitoring.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..core.auth import get_admin_user
from ..models.schemas import (
    UserResponse,
    SessionResponse,
    SessionEventResponse,
    UserWithActivityResponse
)
from ..services.activity_logging_service import activity_logging
from ..services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users-with-activity", response_model=List[UserWithActivityResponse])
async def get_users_with_activity(user: UserResponse = Depends(get_admin_user)):
    """
    Get all users with their activity statistics.
    Admin only endpoint.
    """
    try:
        # Get all users from user service
        users = UserService.list_users()
        
        # Get activity stats
        activity_stats = activity_logging.get_users_with_activity()
        activity_by_uid = {stat["uid"]: stat for stat in activity_stats}
        
        # Merge user data with activity stats
        result = []
        for user_data in users:
            uid = user_data.uid
            stats = activity_by_uid.get(uid, {})
            result.append(UserWithActivityResponse(
                uid=uid,
                email=user_data.email,
                total_sessions=stats.get("total_sessions", 0),
                total_events=stats.get("total_events", 0),
                total_errors=stats.get("total_errors", 0),
                last_activity=stats.get("last_activity")
            ))
        
        # Sort by last_activity descending
        result.sort(key=lambda x: x.last_activity or "", reverse=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{uid}/sessions", response_model=List[SessionResponse])
async def get_user_sessions(uid: str, user: UserResponse = Depends(get_admin_user)):
    """
    Get all sessions for a specific user.
    Admin only endpoint.
    """
    try:
        sessions = activity_logging.get_user_sessions(uid)
        return [SessionResponse(**session) for session in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/events", response_model=List[SessionEventResponse])
async def get_session_events(session_id: str, user: UserResponse = Depends(get_admin_user)):
    """
    Get all events for a specific session.
    Admin only endpoint.
    """
    try:
        events = activity_logging.get_session_events(session_id)
        return [SessionEventResponse(**event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
