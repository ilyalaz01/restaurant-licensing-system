"""
Restaurant Licensing Assessment System - Backend API
SAFE VERSION: Lazy loading to avoid import-time crashes
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from datetime import datetime
import os
import json
import sys
from pathlib import Path

# Initialize FastAPI app (this always works)
app = FastAPI(
    title="Restaurant Licensing API",
    description="AI-powered licensing assessment for restaurants",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Global variables for services (loaded on first use)
_gemini_service = None
_matching_engine = None
_firebase_service = None
_regulations_data = None
_services_loaded = False
_import_error = None

def get_services():
    """
    Lazy load services - only import when actually needed
    This prevents import-time crashes
    """
    global _gemini_service, _matching_engine, _firebase_service
    global _services_loaded, _import_error
    
    if _services_loaded:
        return _gemini_service, _matching_engine, _firebase_service
    
    try:
        # Add current directory to path
        current_dir = Path(__file__).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        # Try to import services
        from services.gemini_service import GeminiService
        from services.matching_engine import MatchingEngine
        from services.firebase_service import FirebaseService
        
        # Initialize services
        _gemini_service = GeminiService()
        _matching_engine = MatchingEngine()
        _firebase_service = FirebaseService()
        
        _services_loaded = True
        return _gemini_service, _matching_engine, _firebase_service
        
    except Exception as e:
        _import_error = str(e)
        print(f"Error loading services: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None, None, None

def get_models():
    """Lazy load models"""
    try:
        from models.business import BusinessDetails, QuestionnaireSubmission
        from models.report import ReportResponse
        return BusinessDetails, QuestionnaireSubmission, ReportResponse
    except Exception as e:
        print(f"Error loading models: {e}", file=sys.stderr)
        return None, None, None

def get_regulations():
    """Lazy load regulations data"""
    global _regulations_data
    
    if _regulations_data is not None:
        return _regulations_data
    
    # Try multiple paths
    current_dir = Path(__file__).parent
    paths_to_try = [
        current_dir / 'data' / 'regulations.json',
        Path('data/regulations.json'),
        Path('../data/regulations.json'),
    ]
    
    for path in paths_to_try:
        try:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    _regulations_data = json.load(f)
                    print(f"✓ Loaded regulations from: {path}", file=sys.stderr)
                    return _regulations_data
        except Exception as e:
            continue
    
    print("Warning: regulations.json not found", file=sys.stderr)
    return None

# ============= API ENDPOINTS =============

@app.get("/")
async def root():
    """Root endpoint - doesn't load any services"""
    return {
        "name": "Restaurant Licensing API",
        "version": "1.0.0",
        "status": "operational",
        "message": "FastAPI working on Vercel!",
        "endpoints": {
            "health": "/api/health",
            "submit_questionnaire": "/api/questionnaire/submit",
            "get_report": "/api/report/{report_id}",
            "regulations": "/api/regulations"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check - tries to load services"""
    
    # Try to load services
    gemini, matching, firebase = get_services()
    regulations = get_regulations()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "gemini": gemini is not None,
            "matching": matching is not None,
            "firebase": firebase is not None,
            "regulations": regulations is not None
        },
        "environment": {
            "GEMINI_API_KEY": bool(os.getenv('GEMINI_API_KEY')),
            "FIREBASE_SERVICE_ACCOUNT": bool(os.getenv('FIREBASE_SERVICE_ACCOUNT')),
            "FIREBASE_DATABASE_URL": bool(os.getenv('FIREBASE_DATABASE_URL')),
        },
        "import_error": _import_error,
        "python_path": sys.path[:3]
    }

@app.get("/api/test-import/{module}")
async def test_import(module: str):
    """Test importing specific modules for debugging"""
    try:
        current_dir = Path(__file__).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        if module == "gemini":
            from services.gemini_service import GeminiService
            return {"success": True, "message": "GeminiService imported successfully"}
        elif module == "firebase":
            from services.firebase_service import FirebaseService
            return {"success": True, "message": "FirebaseService imported successfully"}
        elif module == "matching":
            from services.matching_engine import MatchingEngine
            return {"success": True, "message": "MatchingEngine imported successfully"}
        elif module == "models":
            from models.business import BusinessDetails
            return {"success": True, "message": "Models imported successfully"}
        else:
            return {"success": False, "message": f"Unknown module: {module}"}
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.get("/api/regulations")
async def get_regulations_endpoint():
    """Get all regulations data"""
    regulations = get_regulations()
    
    if not regulations:
        return {
            "success": False,
            "message": "Regulations data not available",
            "regulations": []
        }
    
    return {
        "success": True,
        "regulations": regulations.get("regulations", []),
        "categories": regulations.get("categories", {}),
        "total_count": len(regulations.get("regulations", []))
    }

@app.post("/api/questionnaire/submit")
async def submit_questionnaire(submission: Dict[str, Any]):
    """Submit business questionnaire and generate report"""
    
    # Load services
    gemini, matching, firebase = get_services()
    
    if not all([gemini, matching, firebase]):
        raise HTTPException(
            status_code=503,
            detail=f"Services not available. Error: {_import_error}"
        )
    
    # Load models
    BusinessDetails, QuestionnaireSubmission, _ = get_models()
    
    if not BusinessDetails:
        raise HTTPException(status_code=503, detail="Models not available")
    
    try:
        # Parse submission
        submission_obj = QuestionnaireSubmission(**submission)
        business_details = submission_obj.business_details.calculate_categories()
        
        # Save business to Firebase
        business_result = await firebase.save_business(business_details.dict())
        if not business_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to save business")
        
        business_id = business_result["businessId"]
        
        # Get regulations
        regulations = get_regulations()
        
        # Match regulations
        matched_regulations = matching.match_regulations(
            business_details,
            regulations.get("regulations", []) if regulations else []
        )
        
        # Generate AI report
        ai_report = await gemini.generate_report(
            business_details,
            matched_regulations
        )
        
        # Save report
        report_result = await firebase.save_report(ai_report, business_id)
        if not report_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to save report")
        
        report_id = report_result["reportId"]
        
        return {
            "success": True,
            "message": "Questionnaire submitted successfully",
            "business_id": business_id,
            "report_id": report_id,
            "report_url": f"/report/{report_id}"
        }
        
    except Exception as e:
        print(f"Error processing questionnaire: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """Get generated report by ID"""
    
    _, _, firebase = get_services()
    
    if not firebase:
        raise HTTPException(
            status_code=503,
            detail="Firebase service not available"
        )
    
    try:
        report_result = await firebase.get_report(report_id)
        
        if not report_result["success"]:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "report": report_result["data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting report: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": str(exc.detail) if hasattr(exc, 'detail') else "Not found"
        }
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# No Mangum! Vercel handles ASGI natively