from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..models.schemas import CountResponse, HealthResponse, VersionResponse
from ..services.firebase import increment_visitor_count
from ..services.gemini import generate_emanuel_response

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok"}

@router.get("/version", response_model=VersionResponse)
async def get_version():
    return {"version": "0.1"}

@router.get("/page-load", response_model=CountResponse)
async def track_page_load():
    try:
        count = await increment_visitor_count()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    message: str

@router.post("/emanuel")
async def chat_emanuel(request: ChatRequest):
    return StreamingResponse(generate_emanuel_response(request.message), media_type="text/plain")
