"""
Google Gemini AI Service - Hybrid Approach
AI enhances content while preserving clean structure
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """Service for Google Gemini AI integration - Hybrid approach"""
    
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
        Generate AI-enhanced report with preserved structure
        AI personalizes content but keeps clean formatting
        """
        
        # --- FIX: Calculate BOTH timeline and cost FIRST ---
        estimated_timeline = self._estimate_timeline(business_details, matched_regulations)
        estimated_cost = self._calculate_total_cost(matched_regulations)
            
        if self.mock_mode:
            return self._generate_mock_report(business_details, matched_regulations, estimated_timeline, estimated_cost)
        
        try:
            # --- FIX: Pass BOTH timeline and cost to summary generator ---
            summary = await self._generate_personalized_summary(business_details, matched_regulations, estimated_timeline, estimated_cost)
            
            # Enhance each regulation (preserve structure but personalize text)
            enhanced_regulations = await self._enhance_regulations(business_details, matched_regulations)
            
            # Generate documents and steps
            documents = await self._generate_documents_list(business_details, matched_regulations)
            next_steps = await self._generate_next_steps(business_details, matched_regulations)
            
            # Build report with preserved structure
            report = {
                "summary": summary,
                
                "business": {
                    "business_name": business_details.business_name,
                    "owner_name": business_details.owner_name,
                    "size_sqm": business_details.size_sqm,
                    "seating_capacity": business_details.seating_capacity,
                    "size_category": business_details.size_category,
                    "seating_category": business_details.seating_category,
                    "features": business_details.features,
                    "location_city": getattr(business_details, 'location_city', None),
                    "email": getattr(business_details, 'email', None),
                    "phone": getattr(business_details, 'phone', None)
                },
                
                # Enhanced but structured regulations
                "matched_regulations": enhanced_regulations,
                
                # AI-generated lists
                "required_documents": documents,
                "next_steps": next_steps,
                
                "priority_summary": {
                    "critical": len([r for r in matched_regulations if r.get('priority') == 'critical']),
                    "high": len([r for r in matched_regulations if r.get('priority') == 'high']),
                    "medium": len([r for r in matched_regulations if r.get('priority') == 'medium']),
                    "low": len([r for r in matched_regulations if r.get('priority') == 'low'])
                },
                
                "estimated_timeline": estimated_timeline, # Use the calculated value
                "estimated_cost": estimated_cost, # Use the calculated value
                "ai_generated": True,
                "ai_model": self.model_name
            }
            
            return report
            
        except Exception as e:
            print(f"Error generating AI report: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_report(business_details, matched_regulations, estimated_timeline, estimated_cost)
    
    async def _generate_personalized_summary(self, business: Any, regulations: List[Dict], estimated_timeline: str, estimated_cost: str) -> str:
        """Generate personalized summary paragraph"""
        
        features = ", ".join(business.features) if business.features else "standard operations"
        location = getattr(business, 'location_city', 'Israel')
        
        # --- FIX: Update prompt to use BOTH variables ---
        prompt = f"""You are a helpful business licensing consultant in Israel.

Write a friendly, personalized welcome message for a restaurant owner in ENGLISH.

Business: {business.business_name}
Owner: {business.owner_name}
Location: {location}
Size: {business.size_sqm} sqm
Seating: {business.seating_capacity} seats
Features: {features}
Number of requirements: {len(regulations)}

Your calculated realistic timeline is: {estimated_timeline}
Your total estimated cost range is: {estimated_cost}

Write 2-3 sentences that:
1. Welcome the owner by name and mention their restaurant
2. Acknowledge their specific situation (size, location, features)
3. Give them confidence and state the number of requirements
4. Mention their specific realistic timeline AND the total estimated cost.

Use simple, encouraging language. Write in ENGLISH only.
Do not use markdown or special formatting.
Just write the text directly."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Summary generation failed: {e}")
            # Fallback summary also uses the calculated values
            return (f"Welcome, {business.owner_name}! Based on your restaurant '{business.business_name}' with {business.size_sqm} sqm and features like {features}, "
                    f"you'll need to complete {len(regulations)} licensing requirements. This process typically takes {estimated_timeline} "
                    f"with an estimated total cost of {estimated_cost}.")
    
    async def _enhance_regulations(self, business: Any, regulations: List[Dict]) -> List[Dict]:
        """
        Enhance each regulation with AI while preserving structure
        Keep: title, priority, requirements list, authority
        Enhance: description (make business-specific and friendly)
        """
        
        enhanced = []
        
        # Process in batches to avoid too many API calls
        for reg in regulations[:12]:  # Limit to 12 regulations
            try:
                enhanced_reg = await self._enhance_single_regulation(business, reg)
                enhanced.append(enhanced_reg)
            except Exception as e:
                print(f"Failed to enhance regulation {reg.get('id')}: {e}")
                # Use original if AI fails
                enhanced.append(reg)
        
        return enhanced
    
    async def _enhance_single_regulation(self, business: Any, regulation: Dict) -> Dict:
        """Enhance a single regulation with AI"""
        
        original_title = regulation.get('title', '')
        original_desc = regulation.get('description', '')
        priority = regulation.get('priority', 'medium')
        
        prompt = f"""Rewrite this licensing requirement in business-friendly language for {business.business_name}.

Original requirement:
Title: {original_title}
Description: {original_desc}

Business context:
- Name: {business.business_name}
- Size: {business.size_sqm} sqm
- Features: {', '.join(business.features)}

Task: Rewrite the description in 1-2 sentences that:
1. Explain it in simple, friendly English
2. Make it specific to THIS business (mention their name or features when relevant)
3. Explain WHY it matters
4. Be concise and clear

Write ONLY the description text. No title, no formatting, no bullets.
Do not use ** or other markdown.
Just plain text in English."""

        try:
            response = self.model.generate_content(prompt)
            enhanced_description = response.text.strip()
            
            # Return enhanced regulation with preserved structure
            return {
                "id": regulation.get('id'),
                "title": original_title,  # Keep original title
                "description": enhanced_description,  # AI-enhanced description
                "priority": priority,  # Keep original priority!
                "requirements": regulation.get('requirements', []),  # Keep original list
                "authority": regulation.get('authority'),  # Keep original
                "ai_enhanced": True
            }
            
        except Exception as e:
            print(f"Enhancement failed: {e}")
            return regulation  # Return original on failure
    
    async def _generate_documents_list(self, business: Any, regulations: List[Dict]) -> List[str]:
        """Generate required documents list"""
        
        features = ", ".join(business.features) if business.features else "none"
        
        prompt = f"""List the required documents for licensing {business.business_name} in Israel.

Business details:
- Size: {business.size_sqm} sqm
- Seating: {business.seating_capacity} seats
- Features: {features}

Generate a list of 8-10 required documents in ENGLISH.
Each item should be a single clear sentence.
Be specific to this business.

Format:
- One document per line
- Start each line with the document name
- No numbering, no bullets, no ** formatting
- Just plain text
- Example: "Complete Business License Application Form from the Local Licensing Authority"

Write the list now:"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse into list
            docs = []
            for line in text.split('\n'):
                line = line.strip()
                # Remove any markdown or bullets
                line = line.lstrip('-*•123456789. ')
                if line and len(line) > 10:
                    docs.append(line)
            
            return docs[:10]  # Limit to 10
            
        except Exception as e:
            print(f"Documents generation failed: {e}")
            return [
                "Complete Business License Application Form from the Local Licensing Authority",
                "Property lease agreement or ownership proof",
                "Architectural plans signed by licensed engineer or architect",
                "Fire safety certificate from Fire and Rescue Authority",
                "Health department approval for kitchen and food areas",
                "Environmental impact assessment diagram",
                "Owner's ID and business registration documents",
                "Insurance certificates for business liability"
            ]
    
    async def _generate_next_steps(self, business: Any, regulations: List[Dict]) -> List[str]:
        """Generate actionable next steps"""
        
        features = ", ".join(business.features) if business.features else "none"
        
        prompt = f"""Create a step-by-step action plan for {business.business_name} to get licensed.

Business: {business.business_name}
Size: {business.size_sqm} sqm
Features: {features}

Generate 6-8 actionable steps in ENGLISH.
Make them specific, practical, and in logical order.

Format:
- Number each step (1., 2., etc.)
- Each step should be specific to this business
- Include who to contact where relevant
- Be concise (1-2 sentences per step)
- No ** formatting, just plain text

Example format:
1. Hire a licensed engineer to prepare site plans for your 165 sqm space
2. Contact Haifa Municipality Licensing Department to obtain application forms

Write the steps now:"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse into list
            steps = []
            for line in text.split('\n'):
                line = line.strip()
                if line and len(line) > 10:
                    # Keep the numbering
                    steps.append(line)
            
            return steps[:8]  # Limit to 8
            
        except Exception as e:
            print(f"Steps generation failed: {e}")
            return [
                "1. Hire a licensed engineer or architect to prepare required documentation",
                "2. Contact your local municipal licensing authority to obtain application forms",
                "3. Schedule consultations with Ministry of Health and Fire Department",
                "4. Gather all ownership/lease documents and business registration papers",
                "5. Prepare your kitchen and facilities for health inspection",
                "6. Compile all documents and submit complete application to licensing authority",
                "7. Follow up weekly with authorities and respond promptly to requests",
                "8. Once approved, display your business license prominently at entrance"
            ]

    # --- NEW HELPER METHOD ---
    @staticmethod
    def _parse_cost_range(cost_str: Optional[str]) -> Tuple[int, int]:
        """Parses a cost string like '5,000-15,000 ILS' into (min, max) integers"""
        if not cost_str or "Ongoing" in cost_str:
            return 0, 0
        
        # Clean string: remove notes, currency symbols, commas
        cost_str = re.sub(r"\(.*\)", "", cost_str) # Remove (notes)
        cost_str = cost_str.replace('ILS', '').replace('₪', '').replace(',', '').strip()
        
        if '-' in cost_str:
            parts = cost_str.split('-')
            try:
                low = int(parts[0])
                high = int(parts[1])
                return low, high
            except (ValueError, IndexError):
                return 0, 0
        else:
            try:
                val = int(cost_str)
                return val, val
            except ValueError:
                return 0, 0

    # --- NEW METHOD TO SUM COSTS ---
    def _calculate_total_cost(self, regulations: List[Dict]) -> str:
        """Sum all estimated_cost fields from a list of regulations"""
        min_cost = 0
        max_cost = 0
        for reg in regulations:
            cost_str = reg.get('estimated_cost')
            low, high = self._parse_cost_range(cost_str)
            min_cost += low
            max_cost += high
        
        if max_cost == 0:
            return "N/A (Costs are ongoing or part of build-out)"
        if min_cost == max_cost:
            return f"~₪{max_cost:,.0f} ILS"
        # Format with commas for thousands
        return f"₪{min_cost:,.0f} - ₪{max_cost:,.0f} ILS"

    def _estimate_timeline(self, business: Any, regulations: List[Dict]) -> str:
        """Estimate timeline based on complexity, aligned with sample results"""
        
        # Check for Large / High Complexity first
        # Key triggers: Sprinklers (REG-028), >300 seats
        has_sprinklers = any(r['id'] == 'REG-028' for r in regulations)
        if has_sprinklers or business.size_sqm > 300 or business.seating_capacity > 300:
            return "8-12 months"

        # Check for Medium Complexity
        # Key triggers: Fire Detection (REG-027), >50 seats
        has_fire_detection = any(r['id'] == 'REG-027' for r in regulations)
        if has_fire_detection or business.size_sqm > 50 or business.seating_capacity > 50 or 'alcohol' in business.features:
             return "4-6 months"
        
        # Default to Small / Low Complexity
        return "2-3 months"
    
    def _generate_mock_report(self, business: Any, regulations: List[Dict], estimated_timeline: str, estimated_cost: str) -> Dict[str, Any]:
        """Mock report when API unavailable"""
        return {
            "summary": f"Mock report for {business.business_name}. API key not configured.",
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
                "Health certificates"
            ],
            "next_steps": [
                "1. Configure Gemini API key",
                "2. Restart service",
                "3. Generate real report"
            ],
            "priority_summary": {
                "critical": len([r for r in regulations if r.get('priority') == 'critical']),
                "high": len([r for r in regulations if r.get('priority') == 'high']),
                "medium": len([r for r in regulations if r.get('priority') == 'medium']),
                "low": len([r for r in regulations if r.get('priority') == 'low'])
            },
            "estimated_timeline": estimated_timeline,
            "estimated_cost": estimated_cost,
            "ai_generated": False,
            "mock_mode": True
        }
    
    def _generate_fallback_report(self, business: Any, regulations: List[Dict], estimated_timeline: str, estimated_cost: str) -> Dict[str, Any]:
        """Fallback when AI fails"""
        summary = (f"Welcome, {business.owner_name}! Your restaurant '{business.business_name}' with {business.size_sqm} sqm will need to complete "
                   f"{len(regulations)} licensing requirements. The process typically takes {estimated_timeline} "
                   f"with an estimated total cost of {estimated_cost}.")
        
        return {
            "summary": summary,
            
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
                "Complete Business License Application Form",
                "Property lease or ownership documents",
                "Architectural plans signed by certified professional",
                "Fire safety certificate from Fire Authority",
                "Health department kitchen approval",
                "Environmental impact assessment",
                "Business registration and owner's ID",
                "Insurance certificates"
            ],
            
            "next_steps": [
                "1. Hire a licensed engineer or architect for documentation",
                "2. Contact local municipal licensing authority",
                "3. Schedule Ministry of Health consultation",
                "4. Schedule Fire Department inspection",
                "5. Gather all ownership and registration documents",
                "6. Submit complete application package",
                "7. Follow up weekly with authorities",
                "8. Display license once approved"
            ],
            
            "priority_summary": {
                "critical": len([r for r in regulations if r.get('priority') == 'critical']),
                "high": len([r for r in regulations if r.get('priority') == 'high']),
                "medium": len([r for r in regulations if r.get('priority') == 'medium']),
                "low": len([r for r in regulations if r.get('priority') == 'low'])
            },
            
            "estimated_timeline": estimated_timeline,
            "estimated_cost": estimated_cost,
            "ai_generated": False,
            "fallback_mode": True
        }