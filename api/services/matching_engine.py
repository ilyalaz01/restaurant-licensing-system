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
        
        # === NEW: Threshold-based matching (more accurate than categories) ===
        if "size_threshold" in conditions or "seating_threshold" in conditions:
            size_ok = True
            seating_ok = True
            
            # Check size threshold
            if "size_threshold" in conditions:
                threshold = conditions["size_threshold"]
                size_ok = business.size_sqm >= threshold
            
            # Check seating threshold
            if "seating_threshold" in conditions:
                threshold = conditions["seating_threshold"]
                seating_ok = business.seating_capacity >= threshold
            
            # Determine if BOTH conditions required (AND) or EITHER (OR)
            requires_both = conditions.get("requires_both", False)
            
            if requires_both:
                # Both conditions must be met (AND logic)
                if "size_threshold" in conditions and "seating_threshold" in conditions:
                    return size_ok and seating_ok
                # Only one threshold specified
                elif "size_threshold" in conditions:
                    return size_ok
                else:
                    return seating_ok
            else:
                # Either condition can trigger it (OR logic)
                if "size_threshold" in conditions and "seating_threshold" in conditions:
                    return size_ok or seating_ok
                # Only one threshold specified
                elif "size_threshold" in conditions:
                    return size_ok
                else:
                    return seating_ok
        
        # === LEGACY: Category-based matching (kept for backward compatibility) ===
        if "business_size" in conditions:
            req_size = conditions["business_size"]
            if req_size == "all":
                return True
            if req_size == business.size_category:
                return True
        
        # === Feature-based regulations (IMPROVED) ===
        if "features" in conditions:
            req_features = conditions["features"]
            if isinstance(req_features, list) and len(req_features) > 0:
                # Check if ALL features required (AND logic)
                requires_all = conditions.get("requires_all_features", False)
                
                if requires_all:
                    # Business must have ALL required features
                    return all(feature in business.features for feature in req_features)
                else:
                    # Business must have at least ONE required feature
                    return any(feature in business.features for feature in req_features)
        
        # === Tag-based matching (fallback for features) ===
        tags = regulation.get("tags", [])
        
        # Check if business features match regulation tags
        for feature in business.features:
            if feature in tags:
                return True
            
            # Special feature-to-tag mappings
            feature_tag_map = {
                "alcohol": ["alcohol"],
                "outdoor": ["outdoor", "temporary"],
                "kitchen_gas": ["gas", "safety"],
                "live_music": ["entertainment", "noise", "music"],
                "delivery": ["delivery", "takeout"]
            }
            
            if feature in feature_tag_map:
                if any(tag in tags for tag in feature_tag_map[feature]):
                    return True
        
        # === Size/Seating thresholds via tags (legacy fallback) ===
        # Large businesses
        if business.size_sqm > 150 and "large" in tags:
            return True
        
        # High capacity businesses
        if business.seating_capacity > 50 and "high-capacity" in tags:
            return True
        
        # === General/Cross-sectional regulations ===
        # These apply to all businesses in certain categories
        if regulation.get("category") in ["general_definitions", "cross_sectional"]:
            return True
        
        # Default: does not apply
        return False
    
    def get_regulation_summary(self, matched_regulations: List[Dict]) -> Dict:
        """
        Generate a summary of matched regulations
        
        Args:
            matched_regulations: List of matched regulations
        
        Returns:
            Summary dictionary with counts and breakdowns
        """
        
        summary = {
            "total_count": len(matched_regulations),
            "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_category": {},
            "estimated_total_cost": 0,
        }
        
        for reg in matched_regulations:
            # Count by priority
            priority = reg.get("priority", "low")
            summary["by_priority"][priority] += 1
            
            # Count by category
            category = reg.get("category", "other")
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1
            
            # Sum estimated costs (parse string costs)
            cost_str = reg.get("estimated_cost", "0")
            if cost_str and cost_str != "Ongoing":
                try:
                    # Extract first number from cost string (e.g., "5,000-15,000 ILS" -> 5000)
                    cost_parts = cost_str.replace(",", "").split("-")
                    min_cost = int(''.join(filter(str.isdigit, cost_parts[0])))
                    summary["estimated_total_cost"] += min_cost
                except (ValueError, IndexError):
                    pass
        
        return summary