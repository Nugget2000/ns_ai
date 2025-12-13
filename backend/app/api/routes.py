from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..models.schemas import CountResponse, HealthResponse, VersionResponse
from ..services.firebase import increment_visitor_count
from ..services.gemini import generate_emanuel_response
from ..core.config import settings
from ..core.auth import verify_token
from fastapi import Depends


router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok"}

@router.get("/version", response_model=VersionResponse)
async def get_version():
    return {"version": settings.VERSION}

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
async def chat_emanuel(request: ChatRequest, token: dict = Depends(verify_token)):
    return StreamingResponse(generate_emanuel_response(request.message), media_type="application/x-ndjson")

@router.post("/scrape")
async def run_scraper(token: dict = Depends(verify_token)):
    try:
        # Initialize scraper with default paths (relative to backend/app/services/../../..)
        # We need to be careful with paths. ScraperService defaults to "backend/cache".
        # When running from main.py (uvicorn), the CWD is usually the root of the project or backend.
        # Let's check where uvicorn is run from. Usually it's run from the root or backend dir.
        # If we assume it's run from `backend` or root, we might need to adjust.
        # However, ScraperService uses relative paths.
        # Let's use absolute paths to be safe, or rely on the default if we are confident.
        # The ScraperService defaults: cache_dir="backend/cache", prompt_file="backend/emanuel_prompt.txt"
        # If we run uvicorn from `backend`, then `backend/cache` would be `backend/backend/cache` which is wrong.
        # If we run from root, it's correct.
        # Let's assume we run from root (as per `start.sh` or `docker.sh`).
        
        # To be safer, let's determine the paths based on __file__
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # backend
        cache_dir = os.path.join(base_dir, "cache")
        prompt_file = os.path.join(base_dir, "emanuel_prompt.txt")
        
        from ..services.scraper import ScraperService
        scraper = ScraperService(cache_dir=cache_dir, prompt_file=prompt_file)
        summary = scraper.run()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
