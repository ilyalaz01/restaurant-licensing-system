"""
Gemini AI Service
Generates personalized licensing reports using Google Gemini AI
"""

import google.generativeai as genai
import os
from typing import Dict, List, Any

class GeminiService:
    """Service for generating AI-powered licensing reports"""
    
    def __init__(self):
        """Initialize Gemini with API key"""
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def check_connection(self) -> bool:
        """Check if Gemini is configured"""
        return self.model is not None
    
    async def generate_report(self, business_details: Any, matched_regulations: List[Dict], regenerate: bool = False) -> Dict[str, Any]:
        """
        Generate comprehensive licensing report using AI
        
        Args:
            business_details: Business information
            matched_regulations: List of applicable regulations
            regenerate: Whether this is a regeneration
        
        Returns:
            Complete report dictionary with all sections
        """
        
        if not self.model:
            return self._generate_fallback_report(business_details, matched_regulations)
        
        try:
            # Generate AI summary
            ai_summary = await self._generate_ai_summary(business_details, matched_regulations)
            
            # Extract required documents from regulations
            required_documents = self._extract_required_documents(matched_regulations)
            
            # Generate next steps
            next_steps = self._generate_next_steps(business_details, matched_regulations)
            
            # Build complete report
            report = {
                "summary": ai_summary,
                "business": {
                    "business_name": business_details.business_name,
                    "owner_name": business_details.owner_name,
                    "size_sqm": business_details.size_sqm,
                    "seating_capacity": business_details.seating_capacity,
                    "size_category": business_details.size_category,
                    "seating_category": business_details.seating_category,
                    "features": business_details.features,
                    "location_city": business_details.location_city if hasattr(business_details, 'location_city') else None,
                },
                "matched_regulations": matched_regulations,
                "required_documents": required_documents,
                "next_steps": next_steps,
                "priority_summary": self._generate_priority_summary(matched_regulations),
                "estimated_timeline": self._estimate_timeline(matched_regulations),
                "ai_generated": True,
                "regenerated": regenerate
            }
            
            return report
            
        except Exception as e:
            print(f"Error generating AI report: {e}")
            return self._generate_fallback_report(business_details, matched_regulations)
    
    async def _generate_ai_summary(self, business_details: Any, regulations: List[Dict]) -> str:
        """Generate AI-powered summary of licensing requirements"""
        
        # Build prompt for Gemini
        prompt = self._build_prompt(business_details, regulations)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._generate_fallback_summary(business_details, regulations)
    
    def _build_prompt(self, business: Any, regulations: List[Dict]) -> str:
        """Build detailed prompt for AI"""
        
        # Business characteristics
        features_str = ", ".join(business.features) if business.features else "none"
        
        # Regulations summary
        critical_regs = [r for r in regulations if r.get("priority") == "critical"]
        high_regs = [r for r in regulations if r.get("priority") == "high"]
        
        prompt = f"""You are a licensing expert in Israel helping a restaurant owner understand their licensing requirements.

Business Details:
- Name: {business.business_name}
- Size: {business.size_sqm} square meters ({business.size_category} establishment)
- Seating Capacity: {business.seating_capacity} seats ({business.seating_category} capacity)
- Features: {features_str}
- Location: {getattr(business, 'location_city', 'Not specified')}

Applicable Regulations:
- {len(critical_regs)} critical requirements
- {len(high_regs)} high priority requirements
- {len(regulations)} total regulations apply

Key Regulations:
{self._format_regulations_for_prompt(regulations[:5])}

Task:
Write a clear, professional summary (150-200 words) that:
1. Acknowledges the specific business characteristics
2. Highlights the most critical requirements (2-3 main points)
3. Explains what makes this business's licensing process unique
4. Provides encouraging but realistic timeline expectations
5. Uses accessible language (not legal jargon)

Write in second person ("your restaurant", "you will need to").
Be specific and actionable.
"""
        
        return prompt
    
    def _format_regulations_for_prompt(self, regulations: List[Dict]) -> str:
        """Format regulations for inclusion in prompt"""
        formatted = []
        for reg in regulations:
            formatted.append(f"- {reg.get('title', 'Unnamed')}: {reg.get('description', '')[:100]}...")
        return "\n".join(formatted)
    
    def _generate_fallback_summary(self, business: Any, regulations: List[Dict]) -> str:
        """Generate summary without AI (fallback)"""
        
        features_text = ", ".join(business.features) if business.features else "no special features"
        critical_count = len([r for r in regulations if r.get("priority") == "critical"])
        
        summary = f"""Based on your restaurant "{business.business_name}" with {business.size_sqm} sqm and {business.seating_capacity} seats featuring {features_text}, we've identified {len(regulations)} applicable regulations.

Your establishment is classified as {business.size_category} size with {business.seating_category} seating capacity. You have {critical_count} critical requirements that must be completed before opening.

Key requirements include obtaining certified professional signatures for your business plan, Ministry of Health approval for food safety, and Fire and Rescue Authority clearance. {"Your selected features ("+", ".join(business.features)+") require additional specific approvals." if business.features else ""}

The licensing process typically takes 2-4 months depending on your preparation and local authority responsiveness. We recommend starting with the critical requirements and working with a licensed professional to ensure all documentation is complete."""
        
        return summary
    
    def _extract_required_documents(self, regulations: List[Dict]) -> List[str]:
        """Extract list of required documents from regulations"""
        
        documents = set()
        
        # Standard documents for all
        documents.add("Business license application form")
        documents.add("Site map signed by certified professional")
        documents.add("Environmental diagram signed by certified professional")
        documents.add("Comprehensive business plan")
        documents.add("Proof of ownership or lease agreement")
        documents.add("Owner's ID and company registration")
        
        # Extract from regulations
        for reg in regulations:
            requirements = reg.get("requirements", [])
            for req in requirements:
                if any(keyword in req.lower() for keyword in ["certificate", "approval", "license", "permit", "signed", "document"]):
                    documents.add(req)
        
        return sorted(list(documents))[:12]  # Limit to 12 most important
    
    def _generate_next_steps(self, business: Any, regulations: List[Dict]) -> List[str]:
        """Generate actionable next steps"""
        
        steps = []
        
        # Step 1: Always start with professional
        steps.append("Hire a licensed engineer or architect to prepare required documentation (site maps, environmental diagrams, business plan)")
        
        # Step 2: Based on features
        if "kitchen_gas" in business.features:
            steps.append("Contact licensed gas installer for kitchen gas system inspection and certification")
        
        # Step 3: Fire safety
        if business.size_category == "small":
            steps.append("Prepare fire safety affidavit with certified professional (for small establishments)")
        else:
            steps.append("Schedule Fire and Rescue Authority inspection for your establishment")
        
        # Step 4: Health
        steps.append("Contact Ministry of Health district office to schedule kitchen and facilities inspection")
        
        # Step 5: Special features
        if "alcohol" in business.features:
            steps.append("Verify alcohol serving license requirements with local licensing authority")
        
        if "outdoor" in business.features:
            steps.append("Obtain municipal approval for outdoor seating area including measurements and safety compliance")
        
        if "live_music" in business.features:
            steps.append("Prepare documentation for entertainment venue requirements including sound system safety")
        
        # Step 6: Application
        steps.append("Compile all documents and submit complete application to local licensing authority")
        
        # Step 7: Follow-up
        steps.append("Schedule follow-up meetings with authorities as needed and respond promptly to any requests")
        
        # Step 8: Final
        steps.append("Once approved, display your business license prominently at the entrance")
        
        return steps[:8]  # Limit to 8 steps
    
    def _generate_priority_summary(self, regulations: List[Dict]) -> Dict[str, int]:
        """Count regulations by priority"""
        
        summary = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for reg in regulations:
            priority = reg.get("priority", "low")
            summary[priority] = summary.get(priority, 0) + 1
        
        return summary
    
    def _estimate_timeline(self, regulations: List[Dict]) -> str:
        """Estimate timeline based on regulations"""
        
        critical_count = len([r for r in regulations if r.get("priority") == "critical"])
        total_count = len(regulations)
        
        if critical_count >= 6 or total_count >= 12:
            return "3-4 months (complex case with multiple requirements)"
        elif critical_count >= 4 or total_count >= 8:
            return "2-3 months (standard process with typical requirements)"
        else:
            return "1-2 months (simplified process with basic requirements)"
    
    def _generate_fallback_report(self, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """Generate complete report without AI"""
        
        return {
            "summary": self._generate_fallback_summary(business, regulations),
            "business": {
                "business_name": business.business_name,
                "owner_name": business.owner_name,
                "size_sqm": business.size_sqm,
                "seating_capacity": business.seating_capacity,
                "size_category": business.size_category,
                "seating_category": business.seating_category,
                "features": business.features,
                "location_city": getattr(business, 'location_city', None),
            },
            "matched_regulations": regulations,
            "required_documents": self._extract_required_documents(regulations),
            "next_steps": self._generate_next_steps(business, regulations),
            "priority_summary": self._generate_priority_summary(regulations),
            "estimated_timeline": self._estimate_timeline(regulations),
            "ai_generated": False,
            "regenerated": False
        }
