"""
Restaurant Licensing Assessment System - Backend API
HYBRID VERSION: Imports at top, lazy initialization
This prevents crashes from service initialization at module level
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime
import os
import json
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Import service CLASSES (not instances)
from services.gemini_service import GeminiService
from services.matching_engine import MatchingEngine
from services.firebase_service import FirebaseService

# Import models
from models.business import BusinessDetails, QuestionnaireSubmission
from models.report import ReportResponse

# Initialize FastAPI app
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

# Service instances (initialized on first use)
_gemini_service = None
_matching_engine = None
_firebase_service = None
_regulations_data = None

def get_gemini_service():
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service

def get_matching_engine():
    """Get or create matching engine instance"""
    global _matching_engine
    if _matching_engine is None:
        _matching_engine = MatchingEngine()
    return _matching_engine

def get_firebase_service():
    """Get or create Firebase service instance"""
    global _firebase_service
    if _firebase_service is None:
        _firebase_service = FirebaseService()
    return _firebase_service

def get_regulations():
    """Get or load regulations data"""
    global _regulations_data
    
    if _regulations_data is not None:
        return _regulations_data
    
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
                    return _regulations_data
        except Exception as e:
            continue
    
    print(f"Warning: regulations.json not found", file=sys.stderr)
    return None

# ============= API ENDPOINTS =============

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Restaurant Licensing API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/api/health",
            "submit_questionnaire": "/api/questionnaire/submit",
            "get_report": "/api/report/{report_id}",
            "regulations": "/api/regulations"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    
    # Initialize services on demand
    gemini = get_gemini_service()
    firebase = get_firebase_service()
    regulations = get_regulations()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": firebase.check_connection() if firebase else False,
            "ai": gemini.check_connection() if gemini else False,
            "regulations": regulations is not None
        }
    }

@app.post("/api/questionnaire/submit")
async def submit_questionnaire(submission: QuestionnaireSubmission):
    """Submit business questionnaire and generate report"""
    
    # Get service instances
    gemini = get_gemini_service()
    matching = get_matching_engine()
    firebase = get_firebase_service()
    regulations = get_regulations()
    
    try:
        # Calculate business categories
        business_details = submission.business_details.calculate_categories()
        
        # Save business to Firebase
        business_result = await firebase.save_business(business_details.dict())
        if not business_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to save business data")
        
        business_id = business_result["businessId"]
        
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
        
        # Track analytics
        await firebase.track_event("questionnaire_submitted", {
            "business_size": business_details.size_category,
            "seating_capacity": business_details.seating_category,
            "features_count": len(business_details.features)
        })
        
        return {
            "success": True,
            "message": "Questionnaire submitted successfully",
            "business_id": business_id,
            "report_id": report_id,
            "report_url": f"/report/{report_id}",
            "next_steps": [
                "Review your personalized report",
                "Download or print for your records",
                "Contact professionals for required documents",
                "Begin gathering necessary paperwork"
            ]
        }
        
    except Exception as e:
        print(f"Error processing questionnaire: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """Get generated report by ID"""
    
    firebase = get_firebase_service()
    
    try:
        report_result = await firebase.get_report(report_id)
        
        if not report_result["success"]:
            raise HTTPException(status_code=404, detail="Report not found")
        
        report_data = report_result["data"]
        
        # Get associated business data
        if "businessId" in report_data:
            business_result = await firebase.get_business(report_data["businessId"])
            if business_result["success"]:
                report_data["business"] = business_result["data"]
        
        # Track view
        await firebase.track_event("report_viewed", {"report_id": report_id})
        
        return {
            "success": True,
            "report": report_data,
            "generated_at": report_data.get("generatedAt"),
            "expires_at": report_data.get("generatedAt", 0) + (30 * 24 * 60 * 60 * 1000)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting report: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regulations")
async def get_regulations_endpoint():
    """Get all regulations data"""
    
    regulations = get_regulations()
    
    try:
        if not regulations:
            raise HTTPException(status_code=500, detail="Regulations data not available")
        
        return {
            "success": True,
            "regulations": regulations.get("regulations", []),
            "categories": regulations.get("categories", {}),
            "business_attributes": regulations.get("business_attributes", {}),
            "priority_levels": regulations.get("priority_levels", {}),
            "total_count": len(regulations.get("regulations", []))
        }
        
    except Exception as e:
        print(f"Error getting regulations: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regulations/categories")
async def get_regulation_categories():
    """Get regulation categories"""
    
    regulations = get_regulations()
    
    try:
        if not regulations:
            raise HTTPException(status_code=500, detail="Regulations data not available")
        
        return {
            "success": True,
            "categories": regulations.get("categories", {}),
            "attributes": regulations.get("business_attributes", {})
        }
        
    except Exception as e:
        print(f"Error getting categories: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/regenerate")
async def regenerate_report(data: Dict[str, Any] = Body(...)):
    """Regenerate report with updated parameters"""
    
    gemini = get_gemini_service()
    matching = get_matching_engine()
    firebase = get_firebase_service()
    regulations = get_regulations()
    
    try:
        report_id = data.get("report_id")
        business_id = data.get("business_id")
        
        if not report_id or not business_id:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        # Get business details
        business_result = await firebase.get_business(business_id)
        if not business_result["success"]:
            raise HTTPException(status_code=404, detail="Business not found")
        
        business_data = business_result["data"]
        business_details = BusinessDetails(**business_data)
        
        # Re-match regulations
        matched_regulations = matching.match_regulations(
            business_details,
            regulations.get("regulations", []) if regulations else []
        )
        
        # Generate new AI report
        ai_report = await gemini.generate_report(
            business_details,
            matched_regulations,
            regenerate=True
        )
        
        # Update report
        update_result = await firebase.update_report(report_id, ai_report)
        
        if not update_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to update report")
        
        return {
            "success": True,
            "message": "Report regenerated successfully",
            "report_id": report_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error regenerating report: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "message": str(exc.detail) if hasattr(exc, 'detail') else "Not found"}
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "An unexpected error occurred"}
    )

# No Mangum! Vercel handles ASGI natively