import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
# This uses a service account key file if GOOGLE_APPLICATION_CREDENTIALS is set,
# otherwise it falls back to Application Default Credentials (ADC).
cred = None
if 'GOOGLE_CREDENTIALS_CONTENT' in os.environ:
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_CONTENT')
    creds_dict = json.loads(creds_json)
    cred = credentials.Certificate(creds_dict)
elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
    cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

async def increment_visitor_count() -> int:
    """
    Retrieves the current page load count from Firestore,
    increments it by one, and returns the new count.
    """
    # Reference to the visitor counter document
    doc_ref = db.collection("ns_ai").document("visitor_counter")
    
    # Use a transaction to ensure atomic read-increment-write
    @firestore.transactional
    def increment_counter(transaction):
        snapshot = doc_ref.get(transaction=transaction)
        
        if snapshot.exists:
            current_count = snapshot.get("count")
        else:
            current_count = 0
        
        new_count = current_count + 1
        transaction.set(doc_ref, {"count": new_count})
        return new_count
    
    # Execute the transaction
    transaction = db.transaction()
    count = increment_counter(transaction)
    
    return count
