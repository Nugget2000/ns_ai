from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, TypeAdapter

# --- Model Definitions (Copied from backend/app/models/schemas.py) ---
class FileStoreInfoResponse(BaseModel):
    size_mb: float
    upload_date: Optional[datetime] = None
    display_name: Optional[str] = None

# --- Simulation ---

# Data that caused the error (List of dicts)
mock_data = [
    {'size_mb': 1.57, 'upload_date': datetime(2026, 1, 25, 14, 10, 31, 648419), 'display_name': 'emanuel_scrape_store'},
    {'size_mb': 1.57, 'upload_date': datetime(2026, 1, 25, 20, 19, 31, 545784), 'display_name': 'emanuel_scrape_store'}
]

def verify_fix():
    print("Verifying List[FileStoreInfoResponse]...")
    try:
        # validate_python is used by FastAPI to validate return values
        adapter = TypeAdapter(List[FileStoreInfoResponse])
        result = adapter.validate_python(mock_data)
        print("✅ SUCCESS: Data validated against List[FileStoreInfoResponse]")
        print(result)
    except Exception as e:
        print(f"❌ FAILURE: Could not validate against List[FileStoreInfoResponse]: {e}")

def verify_failure_reproduction():
    print("\nReproducing failure with FileStoreInfoResponse (Single object)...")
    try:
        adapter = TypeAdapter(FileStoreInfoResponse)
        adapter.validate_python(mock_data)
        print("❌ FAILURE: Should have failed validation but didn't.")
    except Exception as e:
        print(f"✅ SUCCESS: Correctly failed validation against single object: {e}")

if __name__ == "__main__":
    verify_failure_reproduction()
    verify_fix()
