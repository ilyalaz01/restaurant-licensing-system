"""
Restaurant Licensing Assessment System - Backend API
FastAPI application for Vercel deployment
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
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
    allow_origins=["*"],  # In production, specify your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_service = GeminiService()
matching_engine = MatchingEngine()
firebase_service = FirebaseService()

# Load regulations data
def load_regulations():
    """Load regulations from JSON file"""
    try:
        with open('data/regulations.json', 'r', encoding='utf-8') as f:
            return json.load(f)
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
            "database": firebase_service.check_connection(),
            "ai": gemini_service.check_connection(),
            "regulations": regulations_data is not None
        }
    }

@app.post("/api/questionnaire/submit")
async def submit_questionnaire(submission: QuestionnaireSubmission):
    """
    Submit business questionnaire and generate report
    """
    try:
        # Calculate business categories
        business_details = submission.business_details.calculate_categories()
        
        # Save business to Firebase
        business_result = await firebase_service.save_business(business_details.dict())
        if not business_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to save business data")
        
        business_id = business_result["businessId"]
        
        # Match regulations based on business details
        matched_regulations = matching_engine.match_regulations(
            business_details,
            regulations_data["regulations"] if regulations_data else []
        )
        
        # Generate AI report
        ai_report = await gemini_service.generate_report(
            business_details,
            matched_regulations
        )
        
        # Save report to Firebase
        report_result = await firebase_service.save_report(ai_report, business_id)
        if not report_result["success"]:
            raise HTTPException(status_code=500, detail="Failed to save report")
        
        report_id = report_result["reportId"]
        
        # Track analytics
        await firebase_service.track_event("questionnaire_submitted", {
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
        print(f"Error processing questionnaire: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """
    Get generated report by ID
    """
    try:
        # Get report from Firebase
        report_result = await firebase_service.get_report(report_id)
        
        if not report_result["success"]:
            raise HTTPException(status_code=404, detail="Report not found")
        
        report_data = report_result["data"]
        
        # Get associated business data
        if "businessId" in report_data:
            business_result = await firebase_service.get_business(report_data["businessId"])
            if business_result["success"]:
                report_data["business"] = business_result["data"]
        
        # Track view
        await firebase_service.track_event("report_viewed", {"report_id": report_id})
        
        return {
            "success": True,
            "report": report_data,
            "generated_at": report_data.get("generatedAt"),
            "expires_at": report_data.get("generatedAt", 0) + (30 * 24 * 60 * 60 * 1000)  # 30 days
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regulations")
async def get_regulations():
    """
    Get all regulations data
    """
    try:
        if not regulations_data:
            raise HTTPException(status_code=500, detail="Regulations data not available")
        
        return {
            "success": True,
            "regulations": regulations_data.get("regulations", []),
            "categories": regulations_data.get("categories", {}),
            "business_attributes": regulations_data.get("business_attributes", {}),
            "priority_levels": regulations_data.get("priority_levels", {}),
            "total_count": len(regulations_data.get("regulations", []))
        }
        
    except Exception as e:
        print(f"Error getting regulations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regulations/categories")
async def get_regulation_categories():
    """
    Get regulation categories
    """
    try:
        if not regulations_data:
            raise HTTPException(status_code=500, detail="Regulations data not available")
        
        return {
            "success": True,
            "categories": regulations_data.get("categories", {}),
            "attributes": regulations_data.get("business_attributes", {})
        }
        
    except Exception as e:
        print(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/regenerate")
async def regenerate_report(data: Dict[str, Any] = Body(...)):
    """
    Regenerate report with updated parameters
    """
    try:
        report_id = data.get("report_id")
        business_id = data.get("business_id")
        
        if not report_id or not business_id:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        # Get business details
        business_result = await firebase_service.get_business(business_id)
        if not business_result["success"]:
            raise HTTPException(status_code=404, detail="Business not found")
        
        business_data = business_result["data"]
        business_details = BusinessDetails(**business_data)
        
        # Re-match regulations
        matched_regulations = matching_engine.match_regulations(
            business_details,
            regulations_data["regulations"] if regulations_data else []
        )
        
        # Generate new AI report
        ai_report = await gemini_service.generate_report(
            business_details,
            matched_regulations,
            regenerate=True
        )
        
        # Update report in Firebase
        update_result = await firebase_service.update_report(report_id, ai_report)
        
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
        print(f"Error regenerating report: {e}")
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

# Vercel handler
handler = app
