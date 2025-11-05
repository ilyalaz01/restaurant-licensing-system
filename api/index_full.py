"""
Restaurant Licensing Assessment System - Vercel API Handler
This file must be in the api folder for Vercel
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import json
import sys
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

# Import services - use relative imports
try:
    from services.gemini_service import GeminiService
    from services.matching_engine import MatchingEngine
    from services.firebase_service import FirebaseService
    from models.business import BusinessDetails, QuestionnaireSubmission
    from models.report import ReportResponse
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports for Vercel
    pass

# Initialize FastAPI app
app = FastAPI(
    title="Restaurant Licensing API",
    description="AI-powered licensing assessment for restaurants",
    version="1.0.0"
)

# Configure CORS - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with error handling
try:
    gemini_service = GeminiService()
    matching_engine = MatchingEngine()
    firebase_service = FirebaseService()
except Exception as e:
    print(f"Service initialization error: {e}")
    gemini_service = None
    matching_engine = None
    firebase_service = None

# Load regulations data
def load_regulations():
    """Load regulations from JSON file"""
    try:
        # Try different paths for Vercel
        possible_paths = [
            'data/regulations.json',
            '../data/regulations.json',
            os.path.join(os.path.dirname(__file__), '..', 'data', 'regulations.json'),
            '/var/task/data/regulations.json',
            '/var/task/api/data/regulations.json'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        print(f"Regulations file not found in any of: {possible_paths}")
        return None
    except Exception as e:
        print(f"Error loading regulations: {e}")
        return None

regulations_data = load_regulations()

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
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": firebase_service.check_connection() if firebase_service else False,
            "ai": gemini_service.check_connection() if gemini_service else False,
            "regulations": regulations_data is not None
        },
        "environment": {
            "has_gemini_key": bool(os.getenv('GEMINI_API_KEY')),
            "has_firebase_config": bool(os.getenv('FIREBASE_SERVICE_ACCOUNT')),
            "python_version": sys.version
        }
    }

@app.post("/api/questionnaire/submit")
async def submit_questionnaire(submission: QuestionnaireSubmission):
    """Submit business questionnaire and generate report"""
    
    if not all([gemini_service, matching_engine, firebase_service]):
        raise HTTPException(status_code=503, detail="Services not initialized")
    
    try:
        # Calculate business categories
        business_details = submission.business_details.calculate_categories()
        
        # Save business to Firebase
        business_result = await firebase_service.save_business(business_details.dict())
        if not business_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to save business data")
        
        business_id = business_result["businessId"]
        
        # Match regulations
        matched_regulations = matching_engine.match_regulations(
            business_details,
            regulations_data["regulations"] if regulations_data else []
        )
        
        # Generate AI report
        ai_report = await gemini_service.generate_report(
            business_details,
            matched_regulations
        )
        
        # Save report
        report_result = await firebase_service.save_report(ai_report, business_id)
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
        print(f"Error processing questionnaire: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """Get generated report by ID"""
    
    if not firebase_service:
        raise HTTPException(status_code=503, detail="Firebase service not initialized")
    
    try:
        # Get report from Firebase
        report_result = await firebase_service.get_report(report_id)
        
        if not report_result["success"]:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "report": report_result["data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regulations")
async def get_regulations():
    """Get all regulations data"""
    try:
        if not regulations_data:
            # Return empty structure if no data
            return {
                "success": True,
                "regulations": [],
                "categories": {},
                "message": "No regulations data loaded"
            }
        
        return {
            "success": True,
            "regulations": regulations_data.get("regulations", []),
            "categories": regulations_data.get("categories", {}),
            "total_count": len(regulations_data.get("regulations", []))
        }
        
    except Exception as e:
        print(f"Error getting regulations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "message": str(exc.detail)}
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "An unexpected error occurred"}
    )

# This is the main handler for Vercel
handler = app
