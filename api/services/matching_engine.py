"""
Matching Engine Service
Matches business details to applicable regulations
"""

from typing import List, Dict, Any

class MatchingEngine:
    """Service for matching regulations to business details"""
    
    def match_regulations(self, business_details: Any, all_regulations: List[Dict]) -> List[Dict]:
        """
        Match applicable regulations based on business details
        
        Args:
            business_details: Business information from questionnaire
            all_regulations: List of all available regulations
        
        Returns:
            List of matched regulations
        """
        
        if not all_regulations:
            return []
        
        matched = []
        
        for regulation in all_regulations:
            # Check if regulation applies to this business
            if self._is_applicable(regulation, business_details):
                matched.append(regulation)
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        matched.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 4))
        
        return matched
    
    def _is_applicable(self, regulation: Dict, business: Any) -> bool:
        """
        Determine if a regulation applies to the business
        
        Args:
            regulation: Regulation to check
            business: Business details
        
        Returns:
            True if applicable, False otherwise
        """
        
        conditions = regulation.get("applicable_conditions", {})
        
        # Always required regulations
        if conditions.get("always_required"):
            return True
        
        # Size-based regulations
        if "business_size" in conditions:
            req_size = conditions["business_size"]
            if req_size == "all":
                return True
            if req_size == business.size_category:
                return True
        
        # Feature-based regulations
        if "features" in conditions:
            req_features = conditions["features"]
            if isinstance(req_features, list):
                for feature in req_features:
                    if feature in business.features:
                        return True
        
        # Check tags for feature matching
        tags = regulation.get("tags", [])
        for feature in business.features:
            if feature in tags:
                return True
            # Special cases
            if feature == "alcohol" and "alcohol" in tags:
                return True
            if feature == "outdoor" and "outdoor" in tags:
                return True
            if feature == "kitchen_gas" and ("gas" in tags or "safety" in tags):
                return True
            if feature == "live_music" and ("entertainment" in tags or "noise" in tags):
                return True
        
        # Size thresholds
        if business.size_sqm > 150 and "large" in tags:
            return True
        
        # Seating capacity thresholds  
        if business.seating_capacity > 50 and "high-capacity" in tags:
            return True
        
        # Default: include if it's a general requirement
        if regulation.get("category") in ["general_definitions", "cross_sectional"]:
            return True
        
        return False
