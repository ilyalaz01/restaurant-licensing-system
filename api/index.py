"""
Minimal FastAPI test for Vercel with Mangum adapter
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # ← THIS IS KEY!
from datetime import datetime

app = FastAPI(title="Restaurant Licensing API - Test")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/api")
async def root():
    return {
        "status": "working",
        "message": "FastAPI with Mangum working!",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "packages_working": True
    }

# CRITICAL: Wrap FastAPI with Mangum
handler = Mangum(app)  # ← Not just 'app'!