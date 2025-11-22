from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI(
    title="NS AI Backend",
    description="Backend for NS AI application",
    version="0.1"
)

# Initialize Firebase
# Note: This uses Application Default Credentials (ADC)
# For production, you should use a service account key file
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/version")
async def get_version():
    return {"version": "0.1"}

@app.get("/page-load")
async def track_page_load():
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
    
    return {"count": count}
