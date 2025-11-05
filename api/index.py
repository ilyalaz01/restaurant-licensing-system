"""
Minimal test API for debugging Vercel deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Create minimal FastAPI app
app = FastAPI(title="Restaurant Licensing API - Test")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "working",
        "message": "Minimal API is running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Handler for Vercel
handler = app
