"""
Google Gemini AI Service
Handles AI-powered report generation
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """Service for Google Gemini AI integration"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = 'gemini-1.5-flash'
        self.mock_mode = False
        
        if not self.api_key:
            print("⚠️ Gemini API key not found - using mock mode")
            self.mock_mode = True
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
                self.mock_mode = True
    
    def _generate_documentation_list(self, business: Any, regulations: List[Dict]) -> List[str]:
        """Generate simple list of required documents"""
        docs = [
            "Business license application form",
            "Property lease or ownership proof",
            "Architectural plans signed by certified engineer",
            "Fire safety certificate",
            "Health department approval",
            "Environmental impact assessment",
            "Owner's ID and company registration",
            "Insurance certificates"
        ]
        
        # Add feature-specific documents
        if 'alcohol' in business.features:
            docs.append("Alcohol serving permit application")
        if 'outdoor' in business.features:
            docs.append("Outdoor seating municipal permit")
        if 'kitchen_gas' in business.features:
            docs.append("Gas installation safety certificate")
        if 'live_music' in business.features:
            docs.append("Entertainment venue license")
        
        return docs[:12]  # Limit to 12 items

    def _generate_next_steps(self, business: Any, regulations: List[Dict]) -> List[str]:
        """Generate actionable next steps"""
        steps = [
            "1. Hire a licensed engineer or architect to prepare required documentation (site maps, environmental diagrams, business plan)",
            "2. Contact your local municipal licensing authority to obtain the application forms",
            "3. Schedule initial consultations with Ministry of Health and Fire Department",
            "4. Gather all ownership/lease documents and company registration papers"
        ]
        
        # Add feature-specific steps
        if 'kitchen_gas' in business.features:
            steps.append("5. Contact a licensed gas installer for kitchen gas system inspection and certification")
        
        if business.size_category == "large" or business.seating_category == "large":
            steps.append(f"{len(steps)+1}. Schedule Fire and Rescue Authority full inspection (required for establishments over 50 sqm or 50 seats)")
        
        if 'outdoor' in business.features:
            steps.append(f"{len(steps)+1}. Submit outdoor seating area plans to municipality for approval")
        
        steps.append(f"{len(steps)+1}. Compile all documents and submit complete application to licensing authority")
        steps.append(f"{len(steps)+1}. Follow up with authorities weekly and respond promptly to any additional requests")
        
        return steps[:8]  # Limit to 8 steps

    def _estimate_timeline(self, business: Any, regulations: List[Dict]) -> str:
        """Estimate completion timeline"""
        base_months = 2
        
        if business.size_sqm > 150:
            base_months += 1
        if len(business.features) > 2:
            base_months += 0.5
        if not business.existing_business:
            base_months += 1
        
        months = int(base_months)
        
        if months <= 2:
            return "1-2 months (simplified process with basic requirements)"
        elif months <= 3:
            return "2-3 months (standard process with typical requirements)"
        else:
            return "3-4 months (complex case with multiple requirements)"
    
    def check_connection(self) -> bool:
        """Check if Gemini service is available"""
        return not self.mock_mode
    
    async def generate_report(self, business_details: Any, matched_regulations: List[Dict], regenerate: bool = False) -> Dict[str, Any]:
        """
        Generate AI-powered report based on business details and regulations
        """
        
        if self.mock_mode:
            return self._generate_mock_report(business_details, matched_regulations)
        
        try:
            # Build the prompt
            prompt = self._build_comprehensive_prompt(business_details, matched_regulations)
            
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            report = self._parse_ai_response(response.text, business_details, matched_regulations)
            
            return report
            
        except Exception as e:
            print(f"Error generating AI report: {e}")
            return self._generate_fallback_report(business_details, matched_regulations)
    
    def _build_comprehensive_prompt(self, business: Any, regulations: List[Dict]) -> str:
        """Build a comprehensive prompt for Gemini"""
        
        # Extract key business details
        features_text = ", ".join(business.features) if business.features else "None specified"
        
        # Summarize regulations
        critical_regs = [r for r in regulations if r.get('priority') == 'critical']
        high_regs = [r for r in regulations if r.get('priority') == 'high']
        
        prompt = f"""
        You are an expert business licensing consultant in Israel, helping restaurant owners navigate complex regulations.
        
        BUSINESS PROFILE:
        - Business Name: {business.business_name}
        - Owner: {business.owner_name}
        - Size: {business.size_sqm} square meters ({business.size_category})
        - Seating Capacity: {business.seating_capacity} seats ({business.seating_category})
        - Special Features: {features_text}
        - New Business: {'Yes' if not business.existing_business else 'No, existing business'}
        - Previous License: {'Yes' if business.previous_license else 'No'}
        
        APPLICABLE REGULATIONS:
        Critical Requirements ({len(critical_regs)} items):
        {self._format_regulations(critical_regs[:5])}
        
        High Priority Requirements ({len(high_regs)} items):
        {self._format_regulations(high_regs[:5])}
        
        TASK: Generate a comprehensive, actionable licensing report that:
        
        1. EXECUTIVE SUMMARY (2-3 sentences)
           - Overview of what this business needs to do
           - Estimated timeline and complexity
        
        2. IMMEDIATE ACTIONS (Top 3-5 urgent steps)
           - What must be done first
           - Who to contact
           - Estimated time for each
        
        3. DOCUMENTATION CHECKLIST
           - Required documents
           - Where to obtain them
           - Approximate costs
        
        4. TIMELINE ROADMAP
           - Week 1: Initial steps
           - Week 2-4: Documentation gathering
           - Month 2-3: Submissions and follow-ups
        
        5. COST BREAKDOWN
           - Government fees
           - Professional services
           - Other expenses
           - Total estimate range
        
        6. PROFESSIONAL TIPS
           - Common mistakes to avoid
           - Money-saving opportunities
           - Expediting strategies
        
        7. SPECIAL CONSIDERATIONS
           - Based on the specific features of this business
           - Any advantages due to size/type
        
        IMPORTANT INSTRUCTIONS:
        - Use clear, simple language (avoid legal jargon)
        - Be specific and actionable (not generic advice)
        - Consider the Israeli context and local requirements
        - Prioritize by urgency and importance
        - Include realistic timeframes
        - Mention relevant authorities (Municipality, Fire Department, Health Ministry)
        
        Format the response with clear headers and bullet points for easy reading.
        Keep the tone professional but friendly and encouraging.
        """
        
        return prompt
    
    


    def _format_regulations(self, regulations: List[Dict]) -> str:
        """Format regulations for the prompt"""
        if not regulations:
            return "- No specific regulations in this category"
        
        formatted = []
        for reg in regulations:
            formatted.append(f"- {reg.get('title', 'Unknown')}: {reg.get('description', '')[:100]}")
        
        return "\n".join(formatted)
    
    def _parse_ai_response(self, ai_text: str, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """Parse AI response into structured report"""
        
        # Calculate total estimated costs
        total_cost = sum(reg.get('estimated_cost', 0) for reg in regulations)
        
        # Create structured report
        report = {
        # Frontend expects "summary" not "executive_summary"
        "summary": self._extract_section(ai_text, "EXECUTIVE SUMMARY", "executive", ai_text[:300]),
        
        # Frontend expects "business" object with all details
        "business": {
            "business_name": business.business_name,
            "owner_name": business.owner_name,
            "size_sqm": business.size_sqm,
            "seating_capacity": business.seating_capacity,
            "size_category": business.size_category,
            "seating_category": business.seating_category,
            "features": business.features,
            "location_city": getattr(business, 'location_city', None),
            "email": getattr(business, 'email', None),
            "phone": getattr(business, 'phone', None)
        },
        
        # Frontend expects "matched_regulations" array
        "matched_regulations": regulations,
        
        # Frontend expects "required_documents" array
        "required_documents": self._generate_documentation_list(business, regulations),
        
        # Frontend expects "next_steps" array
        "next_steps": self._generate_next_steps(business, regulations),
        
        # Additional data
        "priority_summary": {
            "critical": len([r for r in regulations if r.get('priority') == 'critical']),
            "high": len([r for r in regulations if r.get('priority') == 'high']),
            "medium": len([r for r in regulations if r.get('priority') == 'medium']),
            "low": len([r for r in regulations if r.get('priority') == 'low'])
        },
        
        "estimated_timeline": self._estimate_timeline(business, regulations),
        "estimated_cost": total_cost,
        
        "ai_generated": True,
        "regenerated": False
    }
        
        return report
    
    def _extract_section(self, text: str, header: str, keywords: str, default: str = "") -> str:
        """Extract section from AI response"""
        import re
        
        # Try to find section by header
        header_pattern = rf"{header}.*?(?=\n[A-Z]+:|\Z)"
        match = re.search(header_pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0).replace(header, "").strip()[:500]
        
        # Fallback to keyword search
        keyword_pattern = rf".*({keywords}).*"
        matches = re.findall(keyword_pattern, text, re.IGNORECASE)
        if matches:
            return " ".join(matches[:2])[:500]
        
        return default or "Please refer to the detailed requirements listed below."
    
    def _generate_action_items(self, regulations: List[Dict], priority: str) -> List[Dict]:
        """Generate action items from regulations"""
        filtered = [r for r in regulations if r.get('priority') == priority][:5]
        
        return [
            {
                "id": reg.get('id'),
                "title": reg.get('title'),
                "description": reg.get('description'),
                "deadline": "Immediate" if priority == "critical" else "Within 30 days",
                "completed": False
            }
            for reg in filtered
        ]
    
    def _generate_documentation_checklist(self, business: Any, regulations: List[Dict]) -> List[Dict]:
        """Generate documentation checklist"""
        checklist = [
            {"item": "Business registration documents", "required": True, "obtained": False},
            {"item": "Property lease or ownership proof", "required": True, "obtained": False},
            {"item": "Architectural plans signed by engineer", "required": True, "obtained": False},
            {"item": "Environmental impact assessment", "required": business.size_sqm > 100, "obtained": False},
            {"item": "Fire safety certificate", "required": True, "obtained": False},
            {"item": "Health department approval", "required": True, "obtained": False},
        ]
        
        # Add feature-specific documents
        if 'alcohol' in business.features:
            checklist.append({"item": "Alcohol serving permit", "required": True, "obtained": False})
        if 'outdoor' in business.features:
            checklist.append({"item": "Outdoor seating permit", "required": True, "obtained": False})
        if 'live_music' in business.features:
            checklist.append({"item": "Entertainment license", "required": True, "obtained": False})
        
        return checklist
    
    def _generate_timeline_milestones(self, business: Any) -> List[Dict]:
        """Generate timeline milestones"""
        base_date = datetime.now()
        
        milestones = [
            {
                "phase": "Preparation",
                "duration": "Week 1",
                "tasks": ["Gather initial documents", "Contact professionals", "Review requirements"]
            },
            {
                "phase": "Documentation",
                "duration": "Weeks 2-4",
                "tasks": ["Obtain architectural plans", "Complete applications", "Collect certificates"]
            },
            {
                "phase": "Submission",
                "duration": "Month 2",
                "tasks": ["Submit application", "Pay fees", "Schedule inspections"]
            },
            {
                "phase": "Review & Approval",
                "duration": "Month 2-3",
                "tasks": ["Respond to queries", "Complete inspections", "Receive license"]
            }
        ]
        
        return milestones
    
    def _generate_cost_breakdown(self, regulations: List[Dict]) -> Dict[str, int]:
        """Generate cost breakdown"""
        breakdown = {
            "government_fees": 2500,
            "professional_services": 8000,
            "inspections": 1500,
            "documentation": 500,
            "other": 1000
        }
        
        # Add regulation-specific costs
        for reg in regulations:
            if reg.get('estimated_cost', 0) > 0:
                breakdown['regulatory_compliance'] = breakdown.get('regulatory_compliance', 0) + reg['estimated_cost']
        
        return breakdown
    
    def _estimate_total_days(self, business: Any, regulations: List[Dict]) -> int:
        """Estimate total days to completion"""
        base_days = 60
        
        # Adjust based on business complexity
        if business.size_sqm > 150:
            base_days += 15
        if len(business.features) > 3:
            base_days += 10
        if not business.existing_business:
            base_days += 20
        
        return base_days
    
    def _calculate_complexity_score(self, business: Any, regulations: List[Dict]) -> str:
        """Calculate complexity score"""
        score = len(regulations) * 2
        score += len(business.features) * 5
        
        if business.size_sqm > 150:
            score += 10
        if not business.previous_license:
            score += 15
        
        if score < 30:
            return "Low"
        elif score < 60:
            return "Medium"
        else:
            return "High"
    
    def _generate_mock_report(self, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """Generate mock report for testing without API key"""
        return {
            "summary": f"This is a mock report for {business.business_name}. Based on your business size ({business.size_sqm} sqm) and features, you'll need to complete approximately {len(regulations)} regulatory requirements.",
            
            "business": {
                "business_name": business.business_name,
                "owner_name": business.owner_name,
                "size_sqm": business.size_sqm,
                "seating_capacity": business.seating_capacity,
                "size_category": business.size_category,
                "seating_category": business.seating_category,
                "features": business.features
            },
            
            "matched_regulations": regulations,
            "required_documents": self._generate_documentation_list(business, regulations),
            "next_steps": self._generate_next_steps(business, regulations),
            
            "priority_summary": {
                "critical": len([r for r in regulations if r.get('priority') == 'critical']),
                "high": len([r for r in regulations if r.get('priority') == 'high']),
                "medium": len([r for r in regulations if r.get('priority') == 'medium']),
                "low": len([r for r in regulations if r.get('priority') == 'low'])
            },
            
            "estimated_timeline": "2-3 months",
            "ai_generated": False,
            "mock_mode": True
        }
    
    def _generate_fallback_report(self, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """Generate fallback report when AI generation fails"""
        return {
            "summary": (
                f"This fallback report summarizes the key regulatory requirements for {business.business_name}. "
                f"Based on your business size ({business.size_sqm} sqm) and characteristics, approximately "
                f"{len(regulations)} requirements are expected to apply."
            ),

            "business": {
                "business_name": business.business_name,
                "owner_name": business.owner_name,
                "size_sqm": business.size_sqm,
                "seating_capacity": business.seating_capacity,
                "size_category": business.size_category,
                "seating_category": business.seating_category,
                "features": business.features
            },

            "matched_regulations": regulations,
            "required_documents": self._generate_documentation_list(business, regulations),
            "next_steps": self._generate_next_steps(business, regulations),

            "priority_summary": {
                "critical": len([r for r in regulations if r.get('priority') == 'critical']),
                "high": len([r for r in regulations if r.get('priority') == 'high']),
                "medium": len([r for r in regulations if r.get('priority') == 'medium']),
                "low": len([r for r in regulations if r.get('priority') == 'low'])
            },

            "estimated_timeline": "2-3 months",
            "ai_generated": False,
            "fallback_mode": True
        }

