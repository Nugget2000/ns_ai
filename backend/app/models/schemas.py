
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRole(str, Enum):
    PENDING = "pending"
    USER = "user"
    ADMIN = "admin"


class GlucoseUnit(str, Enum):
    MGDL = "mg/dL"
    MMOL = "mmol/L"


class UserSettings(BaseModel):
    """User locale and display preferences."""
    locale: str = "en-US"  # e.g., "sv-SE", "en-US"
    timezone: str = "UTC"  # e.g., "Europe/Stockholm"
    glucose_unit: GlucoseUnit = GlucoseUnit.MGDL


class UserSettingsUpdate(BaseModel):
    """Partial update for user settings."""
    locale: Optional[str] = None
    timezone: Optional[str] = None
    glucose_unit: Optional[GlucoseUnit] = None


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.PENDING

class UserCreate(UserBase):
    uid: str

class UserResponse(UserBase):
    uid: str
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    settings: Optional[UserSettings] = None

class UserUpdate(BaseModel):
    role: Optional[UserRole] = None

class CountResponse(BaseModel):
    count: int

class HealthResponse(BaseModel):
    status: str

class VersionResponse(BaseModel):
    version: str

class FileStoreInfoResponse(BaseModel):
    size_mb: float
    upload_date: Optional[datetime] = None
    display_name: Optional[str] = None


# Activity Logging Schemas
class SessionResponse(BaseModel):
    session_id: str
    uid: str
    email: Optional[str] = None
    started_at: Optional[str] = None  # ISO format string
    last_activity: Optional[str] = None  # ISO format string
    event_count: int = 0
    error_count: int = 0


class SessionEventResponse(BaseModel):
    event_id: str
    session_id: str
    event_type: str
    timestamp: Optional[str] = None  # ISO format string
    data: dict = {}
    error_info: Optional[dict] = None
    stacktrace: Optional[str] = None


class UserWithActivityResponse(BaseModel):
    uid: str
    email: Optional[str] = None
    total_sessions: int = 0
    total_events: int = 0
    total_errors: int = 0
    last_activity: Optional[str] = None  # ISO format string

