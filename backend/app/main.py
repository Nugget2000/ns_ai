import logging
import traceback

import firebase_admin
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.routes import router
from .api.users import router as users_router
from .api.admin import router as admin_router
from .api.nightscout import router as nightscout_router
from .core.config import settings
from .core.logging import setup_logging
from .services.activity_logging_service import activity_logging

# Setup logging
setup_logging()

# Initialize Firebase Admin
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "http://127.0.0.1:5173", "https://nsai.morningmonkey.net"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(admin_router, tags=["admin"])
app.include_router(nightscout_router, prefix="/nightscout", tags=["nightscout"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)

    # Log error to activity logging if we have a session
    try:
        session_id = getattr(request.state, 'session_id', None)
        if session_id:
            activity_logging.log_error(
                session_id=session_id,
                error_type=type(exc).__name__,
                message=str(exc),
                endpoint=str(request.url.path),
                stacktrace=traceback.format_exc()
            )
    except Exception as log_err:
        logging.error(f"Failed to log error to activity logging: {log_err}")

    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
