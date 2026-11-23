
from fastapi import FastAPI
from datetime import datetime, timezone

# Initialize the ReceiptWise application
app = FastAPI(
    title="ReceiptWise API",
    description="Verified Receipt-to-Expense Workflow",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ReceiptWise API",
        "application": "ReceiptWise",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "ReceiptWise",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
