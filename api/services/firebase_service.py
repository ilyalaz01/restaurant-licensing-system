"""
Firebase Service
Handles all Firebase Realtime Database operations
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

load_dotenv()

class FirebaseService:
    """Service for Firebase operations"""
    
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if already initialized
            if not firebase_admin._apps:
                # Get service account from environment variable
                service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT')
                database_url = os.getenv('FIREBASE_DATABASE_URL')
                
                if service_account_json:
                    # Parse the JSON string
                    service_account = json.loads(service_account_json)
                    cred = credentials.Certificate(service_account)
                else:
                    # Try to use default credentials (for local development)
                    print("Warning: No Firebase service account found, using mock mode")
                    self.mock_mode = True
                    return
                
                # Initialize the app
                firebase_admin.initialize_app(cred, {
                    'databaseURL': database_url
                })
                
                self.mock_mode = False
            else:
                self.mock_mode = False
                
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            self.mock_mode = True
    
    def check_connection(self) -> bool:
        """Check if Firebase connection is available"""
        return not self.mock_mode
    
    async def save_business(self, business_data: Dict) -> Dict[str, Any]:
        """Save business details to Firebase"""
        if self.mock_mode:
            return self._mock_save_business(business_data)
        
        try:
            # Generate unique ID
            business_id = f"BUS-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{os.urandom(4).hex()}"
            
            # Add metadata
            business_data['id'] = business_id
            business_data['createdAt'] = datetime.now().isoformat()
            business_data['updatedAt'] = datetime.now().isoformat()
            business_data['status'] = 'active'
            
            # Save to Firebase
            ref = db.reference(f'businesses/{business_id}')
            ref.set(business_data)
            
            return {
                "success": True,
                "businessId": business_id,
                "data": business_data
            }
            
        except Exception as e:
            print(f"Error saving business: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_business(self, business_id: str) -> Dict[str, Any]:
        """Get business by ID"""
        if self.mock_mode:
            return self._mock_get_business(business_id)
        
        try:
            ref = db.reference(f'businesses/{business_id}')
            data = ref.get()
            
            if data:
                return {
                    "success": True,
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "error": "Business not found"
                }
                
        except Exception as e:
            print(f"Error getting business: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def save_report(self, report_data: Dict, business_id: str) -> Dict[str, Any]:
        """Save generated report to Firebase"""
        if self.mock_mode:
            return self._mock_save_report(report_data, business_id)
        
        try:
            # Generate unique ID
            report_id = f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{os.urandom(4).hex()}"
            
            # Add metadata
            report_data['id'] = report_id
            report_data['businessId'] = business_id
            report_data['generatedAt'] = datetime.now().isoformat()
            
            # Save to Firebase
            ref = db.reference(f'reports/{report_id}')
            ref.set(report_data)
            
            # Update business with latest report ID
            business_ref = db.reference(f'businesses/{business_id}')
            business_ref.update({
                'latestReportId': report_id,
                'updatedAt': datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "reportId": report_id,
                "data": report_data
            }
            
        except Exception as e:
            print(f"Error saving report: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_report(self, report_id: str) -> Dict[str, Any]:
        """Get report by ID"""
        if self.mock_mode:
            return self._mock_get_report(report_id)
        
        try:
            ref = db.reference(f'reports/{report_id}')
            data = ref.get()
            
            if data:
                return {
                    "success": True,
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "error": "Report not found"
                }
                
        except Exception as e:
            print(f"Error getting report: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_report(self, report_id: str, updates: Dict) -> Dict[str, Any]:
        """Update existing report"""
        if self.mock_mode:
            return {"success": True, "reportId": report_id}
        
        try:
            ref = db.reference(f'reports/{report_id}')
            updates['updatedAt'] = datetime.now().isoformat()
            ref.update(updates)
            
            return {
                "success": True,
                "reportId": report_id
            }
            
        except Exception as e:
            print(f"Error updating report: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def track_event(self, event_type: str, event_data: Dict = None) -> Dict[str, Any]:
        """Track analytics event"""
        if self.mock_mode:
            return {"success": True}
        
        try:
            # Generate event ID
            event_id = f"EVT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{os.urandom(4).hex()}"
            
            # Create event data
            event = {
                'id': event_id,
                'type': event_type,
                'data': event_data or {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to Firebase
            ref = db.reference(f'analytics/events/{event_id}')
            ref.set(event)
            
            # Update daily stats
            today = datetime.now().strftime('%Y-%m-%d')
            stats_ref = db.reference(f'analytics/daily/{today}/{event_type}')
            current = stats_ref.get() or 0
            stats_ref.set(current + 1)
            
            return {"success": True}
            
        except Exception as e:
            print(f"Error tracking event: {e}")
            return {"success": False, "error": str(e)}
    
    _mock_reports_store = {}  # Class variable to store reports
    _mock_business_store = {}  # Class variable to store businesses
    
    def _mock_save_business(self, business_data: Dict) -> Dict[str, Any]:
        """Mock save business for testing"""
        business_id = f"MOCK-BUS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Store in memory
        self._mock_business_store[business_id] = {
            **business_data,
            "id": business_id
        }
        
        return {
            "success": True,
            "businessId": business_id,
            "data": business_data
        }
    
    def _mock_get_business(self, business_id: str) -> Dict[str, Any]:
        """Mock get business for testing"""
        if business_id in self._mock_business_store:
            return {
                "success": True,
                "data": self._mock_business_store[business_id]
            }
        
        return {
            "success": True,
            "data": {
                "id": business_id,
                "business_name": "Mock Restaurant",
                "mock": True
            }
        }
    
    def _mock_save_report(self, report_data: Dict, business_id: str) -> Dict[str, Any]:
        """Mock save report for testing"""
        report_id = f"MOCK-RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Store the COMPLETE report in memory
        self._mock_reports_store[report_id] = {
            **report_data,  # ← Save ALL the fields!
            "id": report_id,
            "businessId": business_id
        }
        
        return {
            "success": True,
            "reportId": report_id,
            "data": report_data
        }
    
    def _mock_get_report(self, report_id: str) -> Dict[str, Any]:
        """Mock get report for testing"""
        # Try to get from memory store
        if report_id in self._mock_reports_store:
            return {
                "success": True,
                "data": self._mock_reports_store[report_id]
            }
        
        # Fallback to a complete mock structure
        return {
            "success": True,
            "data": {
                "id": report_id,
                "mock": True,
                "summary": "This is a mock report. Firebase is in mock mode (no real database connection). The report would normally show complete AI-generated analysis here.",
                "business": {
                    "business_name": "Mock Restaurant",
                    "owner_name": "Mock Owner",
                    "size_sqm": 100,
                    "seating_capacity": 40,
                    "size_category": "medium",
                    "seating_category": "standard",
                    "features": []
                },
                "matched_regulations": [
                    {
                        "id": "MOCK-REG-001",
                        "title": "Mock Regulation",
                        "description": "This is a mock regulation for testing",
                        "priority": "high"
                    }
                ],
                "required_documents": [
                    "Business license application",
                    "Property documents",
                    "Health certificate"
                ],
                "next_steps": [
                    "1. Connect real Firebase database",
                    "2. Submit questionnaire again",
                    "3. Get real AI-generated report"
                ],
                "priority_summary": {
                    "critical": 0,
                    "high": 1,
                    "medium": 0,
                    "low": 0
                },
                "estimated_timeline": "2-3 months"
            }
        }
