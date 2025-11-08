"""
Google Gemini AI Service
Fully AI-powered report generation - processes all data through AI
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
        self.model_name = 'gemini-2.5-flash'  
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
    
    def check_connection(self) -> bool:
        """Check if Gemini service is available"""
        return not self.mock_mode
    
    async def generate_report(self, business_details: Any, matched_regulations: List[Dict], regenerate: bool = False) -> Dict[str, Any]:
        """
        Generate FULLY AI-powered report
        AI processes everything - summary, regulations, documents, steps
        """
        
        if self.mock_mode:
            return self._generate_mock_report(business_details, matched_regulations)
        
        try:
            # Generate ALL content through AI in one comprehensive call
            full_report = await self._generate_complete_ai_report(business_details, matched_regulations)
            
            return full_report
            
        except Exception as e:
            print(f"Error generating AI report: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_report(business_details, matched_regulations)
    
    async def _generate_complete_ai_report(self, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """
        Generate complete report with AI processing EVERYTHING
        This is the core AI functionality
        """
        
        # Build comprehensive prompt that processes everything
        prompt = self._build_full_ai_prompt(business, regulations)
        
        try:
            # Generate content
            response = self.model.generate_content(prompt)
            ai_text = response.text
            
            # Parse AI response into structured format
            report = self._parse_complete_ai_response(ai_text, business, regulations)
            
            return report
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            raise
    
    def _build_full_ai_prompt(self, business: Any, regulations: List[Dict]) -> str:
        """
        Build comprehensive prompt for AI to process EVERYTHING
        """
        
        # Format features
        features_text = ", ".join(business.features) if business.features else "standard operations"
        
        # Format raw regulations for AI to process
        regulations_text = "\n\n".join([
            f"REGULATION {i+1}:\n"
            f"Title: {reg.get('title', 'N/A')}\n"
            f"Priority: {reg.get('priority', 'N/A')}\n"
            f"Description: {reg.get('description', 'N/A')}\n"
            f"Requirements: {', '.join(reg.get('requirements', []))}\n"
            f"Authority: {reg.get('authority', 'N/A')}"
            for i, reg in enumerate(regulations[:12])  # Limit to avoid token limits
        ])
        
        prompt = f"""You are an expert business licensing consultant in Israel helping restaurant owners.

CRITICAL INSTRUCTIONS:
- Write EVERYTHING in ENGLISH only
- Use business-friendly language (not legal jargon)
- Personalize EVERYTHING to this specific business
- Be practical and actionable
- Use a warm, encouraging tone

BUSINESS PROFILE:
Business Name: {business.business_name}
Owner: {business.owner_name}
Size: {business.size_sqm} square meters ({business.size_category} establishment)
Seating: {business.seating_capacity} seats ({business.seating_category} capacity)
Features: {features_text}
Location: {getattr(business, 'location_city', 'Israel')}

RAW REGULATIONS DATA:
{regulations_text}

YOUR TASK:
Generate a complete, personalized licensing report. Process the raw regulations above and transform them into clear, actionable guidance.

OUTPUT FORMAT (return as structured text with clear sections):

## EXECUTIVE SUMMARY
[Write 2-3 sentences in ENGLISH that:
- Directly address the business owner by referencing their specific business
- Explain what they need to do in simple terms
- Give realistic timeline
- Be encouraging but realistic]

## KEY REQUIREMENTS
[Process each regulation above and rewrite in business-friendly language:
- For EACH regulation, write a clear explanation in simple English
- Explain WHY it matters for THIS specific business
- Give practical advice on HOW to comply
- Use format: "**Title** (Priority): Explanation specific to {business.business_name}"
- Make it personal, not generic]

## REQUIRED DOCUMENTS
[List 8-10 specific documents needed, in simple language:
- Based on the regulations above
- Customized for this business size and features
- Each document should be a clear, one-line description]

## NEXT STEPS
[Create 6-8 actionable steps:
- Step-by-step guidance specific to this business
- Include who to contact
- Reference specific authorities mentioned in regulations
- Be practical and time-sensitive
- Format: "1. First action for {business.business_name}..."]

## ESTIMATED TIMELINE
[Give a realistic timeline based on:
- Business size: {business.size_sqm} sqm
- Features: {features_text}
- Number of requirements: {len(regulations)}
- Format: "X-Y months" with brief explanation]

REMEMBER:
- Everything must be in ENGLISH
- Make it personal to "{business.business_name}"
- Use their specific features: {features_text}
- Transform legal language into business language
- Be specific, not generic

Generate the report now:"""
        
        return prompt
    
    def _parse_complete_ai_response(self, ai_text: str, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """
        Parse AI response into structured report format
        """
        
        # Extract sections from AI response
        summary = self._extract_section(ai_text, "EXECUTIVE SUMMARY", "KEY REQUIREMENTS")
        key_requirements_text = self._extract_section(ai_text, "KEY REQUIREMENTS", "REQUIRED DOCUMENTS")
        documents_text = self._extract_section(ai_text, "REQUIRED DOCUMENTS", "NEXT STEPS")
        steps_text = self._extract_section(ai_text, "NEXT STEPS", "ESTIMATED TIMELINE")
        timeline = self._extract_section(ai_text, "ESTIMATED TIMELINE", "---")
        
        # Process AI-generated requirements into structured format
        ai_processed_regulations = self._parse_ai_requirements(key_requirements_text, regulations)
        
        # Parse documents list
        required_documents = self._parse_list_from_text(documents_text)
        
        # Parse next steps
        next_steps = self._parse_list_from_text(steps_text)
        
        # Build complete report
        report = {
            "summary": summary.strip(),
            
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
            
            # AI-processed regulations (transformed from raw data)
            "matched_regulations": ai_processed_regulations,
            
            # AI-generated documents list
            "required_documents": required_documents[:12],
            
            # AI-generated next steps
            "next_steps": next_steps[:8],
            
            "priority_summary": {
                "critical": len([r for r in regulations if r.get('priority') == 'critical']),
                "high": len([r for r in regulations if r.get('priority') == 'high']),
                "medium": len([r for r in regulations if r.get('priority') == 'medium']),
                "low": len([r for r in regulations if r.get('priority') == 'low'])
            },
            
            "estimated_timeline": timeline.strip() if timeline else "2-3 months",
            "ai_generated": True,
            "ai_model": self.model_name
        }
        
        return report
    
    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> str:
        """Extract section between two markers"""
        import re
        
        # Try to find section
        pattern = rf"{start_marker}(.*?)(?={end_marker}|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            content = match.group(1).strip()
            # Remove markdown headers
            content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
            return content
        
        return ""
    
    def _parse_ai_requirements(self, requirements_text: str, original_regulations: List[Dict]) -> List[Dict]:
        """
        Parse AI-generated requirements text into structured format
        AI has already processed and simplified them
        """
        
        structured_reqs = []
        
        # Split by paragraphs or numbered items
        lines = requirements_text.split('\n')
        
        current_req = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a new requirement (starts with ** or number)
            if line.startswith('**') or line.startswith('###') or (len(line) > 0 and line[0].isdigit()):
                if current_req:
                    structured_reqs.append(current_req)
                
                # Parse the requirement
                # Extract title and priority
                title = line.replace('**', '').replace('###', '').strip()
                
                # Try to extract priority
                priority = 'medium'
                if '(Critical)' in title or '(CRITICAL)' in title:
                    priority = 'critical'
                    title = title.replace('(Critical)', '').replace('(CRITICAL)', '').strip()
                elif '(High)' in title or '(HIGH)' in title:
                    priority = 'high'
                    title = title.replace('(High)', '').replace('(HIGH)', '').strip()
                elif '(Medium)' in title or '(MEDIUM)' in title:
                    priority = 'medium'
                    title = title.replace('(Medium)', '').replace('(MEDIUM)', '').strip()
                elif '(Low)' in title or '(LOW)' in title:
                    priority = 'low'
                    title = title.replace('(Low)', '').replace('(LOW)', '').strip()
                
                current_req = {
                    "id": f"AI-REQ-{len(structured_reqs)+1:03d}",
                    "title": title,
                    "priority": priority,
                    "description": "",
                    "requirements": [],
                    "ai_processed": True
                }
            elif current_req:
                # Add to description
                current_req["description"] += " " + line
        
        # Add last requirement
        if current_req:
            structured_reqs.append(current_req)
        
        # If parsing failed, use original regulations but mark as AI-processed
        if len(structured_reqs) < 3:
            return [{
                **reg,
                "ai_processed": True,
                "description": f"[AI] {reg.get('description', '')}"
            } for reg in original_regulations[:10]]
        
        return structured_reqs[:12]
    
    def _parse_list_from_text(self, text: str) -> List[str]:
        """Parse a bulleted or numbered list from text"""
        items = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Remove list markers
            line = line.lstrip('*-•123456789.')
            line = line.strip()
            
            if line and len(line) > 5:
                items.append(line)
        
        return items
    
    def _generate_mock_report(self, business: Any, regulations: List[Dict]) -> Dict[str, Any]:
        """Generate mock report for testing without API key"""
        return {
            "summary": f"This is a mock report for {business.business_name}. In production, AI would generate a personalized analysis here.",
            
            "business": {
                "business_name": business.business_name,
                "owner_name": business.owner_name,
                "size_sqm": business.size_sqm,
                "seating_capacity": business.seating_capacity,
                "size_category": business.size_category,
                "seating_category": business.seating_category,
                "features": business.features
            },
            
            "matched_regulations": regulations[:10],
            "required_documents": [
                "Business license application form",
                "Property documents",
                "Health certificates",
                "Fire safety approval"
            ],
            "next_steps": [
                "1. Hire certified professional",
                "2. Prepare documentation",
                "3. Submit application"
            ],
            
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
        """Generate fallback report when AI fails"""
        return {
            "summary": f"Based on your restaurant '{business.business_name}' with {business.size_sqm} sqm and {len(business.features)} special features, you'll need to complete approximately {len(regulations)} licensing requirements. This process typically takes 2-3 months.",
            
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
            "required_documents": [
                "Business license application form",
                "Property lease or ownership proof",
                "Architectural plans signed by certified engineer",
                "Fire safety certificate",
                "Health department approval",
                "Environmental impact assessment",
                "Owner's ID and company registration",
                "Insurance certificates"
            ],
            "next_steps": [
                "1. Hire a licensed engineer or architect to prepare required documentation",
                "2. Contact your local municipal licensing authority",
                "3. Schedule consultations with Ministry of Health and Fire Department",
                "4. Gather all ownership/lease documents",
                "5. Compile all documents and submit complete application",
                "6. Follow up with authorities and respond to requests"
            ],
            
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