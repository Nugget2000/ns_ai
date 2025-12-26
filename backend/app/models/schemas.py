
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRole(str, Enum):
    PENDING = "pending"
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.PENDING

class UserCreate(UserBase):
    uid: str

class UserResponse(UserBase):
    uid: str
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

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
