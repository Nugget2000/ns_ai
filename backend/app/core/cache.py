from datetime import datetime
from google.cloud import firestore
from .config import settings

PREFIX = "ns_insight_cache"

db = None
if settings.CACHE_ENABLED and settings.GCP_PROJECT_ID:
    db = firestore.Client(project=settings.GCP_PROJECT_ID)

def get_cache(key: str):
    """Hämtar ett värde från cachen."""
    if not db:
        return None
    doc_ref = db.collection(PREFIX).document(key)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("value")
    return None

def set_cache(key: str, value: any):
    """Sparar ett värde i cachen."""
    # Add cached_at timestamp to the value if it's a list of dictionaries
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        for item in value:
            item['cached_at'] = datetime.now().isoformat()

    if not db:
        return
    doc_ref = db.collection(PREFIX).document(key)
    doc_ref.set({"value": value})