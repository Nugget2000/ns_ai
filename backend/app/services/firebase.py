import firebase_admin
from firebase_admin import firestore

# Initialize Firebase
# Note: This uses Application Default Credentials (ADC)
# For production, you should use a service account key file
if not firebase_admin._apps:
    firebase_admin.initialize_app()

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
