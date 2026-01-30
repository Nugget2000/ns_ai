from datetime import datetime
from google.cloud import firestore
from .config import settings

PREFIX = "ns_insight_cache"

db = None
if settings.CACHE_ENABLED and settings.GCP_PROJECT_ID:
    db = firestore.Client(project=settings.GCP_PROJECT_ID)

def get_cache(key: str, user_id: str = None):
    """Hämtar ett värde från cachen.
    
    Args:
        key: The cache key.
        user_id: Optional user ID to scope the cache to a specific user.
                 If provided, the cache is stored in a user-specific subcollection.
    """
    if not db:
        return None
    
    if user_id:
        # User-specific cache: ns_insight_cache/{user_id}/cache/{key}
        doc_ref = db.collection(PREFIX).document(user_id).collection("cache").document(key)
    else:
        # Global cache: ns_insight_cache/{key}
        doc_ref = db.collection(PREFIX).document(key)
    
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("value")
    return None

def set_cache(key: str, value: any, user_id: str = None):
    """Sparar ett värde i cachen.
    
    Args:
        key: The cache key.
        value: The value to cache.
        user_id: Optional user ID to scope the cache to a specific user.
                 If provided, the cache is stored in a user-specific subcollection.
    """
    # Add cached_at timestamp to the value if it's a list of dictionaries
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        for item in value:
            item['cached_at'] = datetime.now().isoformat()

    if not db:
        return
    
    if user_id:
        # User-specific cache: ns_insight_cache/{user_id}/cache/{key}
        doc_ref = db.collection(PREFIX).document(user_id).collection("cache").document(key)
    else:
        # Global cache: ns_insight_cache/{key}
        doc_ref = db.collection(PREFIX).document(key)
    
    doc_ref.set({"value": value})