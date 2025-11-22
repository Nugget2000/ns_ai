from pydantic import BaseModel

class CountResponse(BaseModel):
    count: int

class HealthResponse(BaseModel):
    status: str

class VersionResponse(BaseModel):
    version: str
