"""
Debug version - will show what's actually failing
"""
import sys
import traceback

print("=== STARTING DEBUG ===", file=sys.stderr)

try:
    print("Step 1: Importing FastAPI...", file=sys.stderr)
    from fastapi import FastAPI
    print("✓ FastAPI imported", file=sys.stderr)
    
    print("Step 2: Importing Mangum...", file=sys.stderr)
    from mangum import Mangum
    print("✓ Mangum imported", file=sys.stderr)
    
    print("Step 3: Creating FastAPI app...", file=sys.stderr)
    app = FastAPI()
    print("✓ FastAPI app created", file=sys.stderr)
    
    print("Step 4: Adding CORS...", file=sys.stderr)
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("✓ CORS added", file=sys.stderr)
    
    print("Step 5: Adding routes...", file=sys.stderr)
    @app.get("/")
    def home():
        return {"status": "working", "message": "FastAPI with Mangum!"}
    
    @app.get("/api")
    def api_root():
        return {"status": "working", "message": "API endpoint!"}
    
    @app.get("/api/health")
    def health():
        return {"status": "healthy"}
    
    print("✓ Routes added", file=sys.stderr)
    
    print("Step 6: Creating Mangum handler...", file=sys.stderr)
    handler = Mangum(app, lifespan="off")
    print("✓ Mangum handler created", file=sys.stderr)
    
    print("=== DEBUG COMPLETE - ALL STEPS PASSED ===", file=sys.stderr)
    
except Exception as e:
    print(f"❌ ERROR at step: {e}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    raise