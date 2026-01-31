from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..models.schemas import CountResponse, HealthResponse, VersionResponse, FileStoreInfoResponse
from ..services.firebase import increment_visitor_count
from ..services.emanuel import generate_emanuel_response, get_file_store_info
from ..services.activity_logging_service import activity_logging
from ..core.config import settings
from ..core.auth import verify_token, get_active_user
from fastapi import Depends
import time
import json
import traceback


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


async def logged_emanuel_response(message: str, session_id: str):
    """
    Wrapper generator that logs chat message and response events.
    """
    start_time = time.time()
    full_response = ""
    input_tokens = None
    output_tokens = None
    
    # Log the user's chat message
    activity_logging.log_chat_message(session_id, message)
    
    try:
        async for chunk in generate_emanuel_response(message):
            yield chunk
            
            # Parse the chunk to capture response and metrics
            try:
                data = json.loads(chunk.strip())
                if data.get("type") == "content":
                    full_response += data.get("text", "")
                elif data.get("type") == "usage":
                    input_tokens = data.get("input_tokens")
                    output_tokens = data.get("output_tokens")
                elif data.get("type") == "error":
                    # Log error event
                    activity_logging.log_error(
                        session_id=session_id,
                        error_type="chat_error",
                        message=data.get("text", "Unknown error"),
                        endpoint="/emanuel"
                    )
            except json.JSONDecodeError:
                pass
        
        # Log the complete response at the end
        duration_ms = int((time.time() - start_time) * 1000)
        activity_logging.log_chat_response(
            session_id=session_id,
            response=full_response,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            duration_ms=duration_ms
        )
    except Exception as e:
        # Log error with stacktrace
        activity_logging.log_error(
            session_id=session_id,
            error_type=type(e).__name__,
            message=str(e),
            endpoint="/emanuel",
            stacktrace=traceback.format_exc()
        )
        raise


@router.post("/emanuel")
async def chat_emanuel(chat_request: ChatRequest, request: Request, user: dict = Depends(get_active_user)):
    session_id = getattr(request.state, 'session_id', None)
    if session_id:
        return StreamingResponse(
            logged_emanuel_response(chat_request.message, session_id),
            media_type="application/x-ndjson"
        )
    else:
        # Fallback if no session (shouldn't happen normally)
        return StreamingResponse(
            generate_emanuel_response(chat_request.message),
            media_type="application/x-ndjson"
        )

from typing import List

@router.get("/emanuel/file-store-info", response_model=List[FileStoreInfoResponse])
async def get_file_store_info_endpoint(user: dict = Depends(get_active_user)):
    """Get information about the file search store."""
    try:
        info = get_file_store_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scrape")
async def run_scraper(user: dict = Depends(get_active_user)):
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
