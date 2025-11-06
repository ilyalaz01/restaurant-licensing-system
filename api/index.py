from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

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
        "message": "FastAPI on Vercel - No Mangum!",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api")
async def api_root():
    return {"status": "working", "message": "API endpoint!"}

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# No Mangum! Just the FastAPI app
# Vercel's @vercel/python runtime handles ASGI