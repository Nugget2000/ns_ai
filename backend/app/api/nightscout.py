from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..services.nightscout_service import test_nightscout_connection
from ..services.user_service import UserService
from ..models.schemas import UserResponse
from ..core.auth import get_current_user

router = APIRouter()


class NightscoutTestRequest(BaseModel):
    """Request body for testing a Nightscout URL before saving."""
    url: str


class NightscoutTestResponse(BaseModel):
    """Response from testing a Nightscout connection."""
    success: bool
    sgv: Optional[int] = None
    timestamp: Optional[str] = None
    time_ago: Optional[str] = None
    error: Optional[str] = None


@router.post("/test", response_model=NightscoutTestResponse)
async def test_nightscout(
    request: NightscoutTestRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Test a Nightscout URL before saving it.
    Returns the current glucose reading and time since last reading.
    """
    result = test_nightscout_connection(request.url)
    return NightscoutTestResponse(**result)


@router.post("/test-saved", response_model=NightscoutTestResponse)
async def test_saved_nightscout(
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Test the saved Nightscout URL from user settings.
    Returns the current glucose reading and time since last reading.
    """
    settings = UserService.get_user_settings(current_user.uid)
    
    if not settings.nightscout_url:
        return NightscoutTestResponse(
            success=False,
            error="No Nightscout URL configured in settings"
        )
    
    result = test_nightscout_connection(settings.nightscout_url)
    return NightscoutTestResponse(**result)
