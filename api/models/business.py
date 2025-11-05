"""
Business Models
Pydantic models for business data validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class BusinessSize(str, Enum):
    """Business size categories"""
    SMALL = "small"
    MEDIUM = "medium" 
    LARGE = "large"

class SeatingCapacity(str, Enum):
    """Seating capacity categories"""
    INTIMATE = "intimate"
    STANDARD = "standard"
    LARGE = "large"

class BusinessFeature(str, Enum):
    """Available business features"""
    ALCOHOL = "alcohol"
    DELIVERY = "delivery"
    OUTDOOR = "outdoor"
    KITCHEN_GAS = "kitchen_gas"
    LIVE_MUSIC = "live_music"

class BusinessDetails(BaseModel):
    """Business details from questionnaire"""
    
    # Basic Information
    business_name: str = Field(..., min_length=2, max_length=100)
    owner_name: str = Field(..., min_length=2, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    
    # Size and Capacity
    size_sqm: float = Field(..., gt=0, le=500)
    seating_capacity: int = Field(..., ge=0, le=500)
    
    # Features
    features: List[str] = Field(default=[])
    
    # Additional Information
    location_city: Optional[str] = None
    planned_opening_date: Optional[str] = None
    existing_business: bool = Field(default=False)
    previous_license: bool = Field(default=False)
    
    # Computed fields
    size_category: Optional[str] = None
    seating_category: Optional[str] = None
    
    @validator('size_sqm')
    def validate_size(cls, v):
        """Validate and categorize business size"""
        if v <= 0:
            raise ValueError("Size must be positive")
        return v
    
    @validator('seating_capacity')
    def validate_seating(cls, v):
        """Validate seating capacity"""
        if v < 0:
            raise ValueError("Seating capacity cannot be negative")
        return v
    
    def calculate_categories(self):
        """Calculate size and seating categories"""
        # Size category
        if self.size_sqm <= 50:
            self.size_category = "small"
        elif self.size_sqm <= 100:
            self.size_category = "medium"
        else:
            self.size_category = "large"
        
        # Seating category
        if self.seating_capacity <= 20:
            self.seating_category = "intimate"
        elif self.seating_capacity <= 50:
            self.seating_category = "standard"
        else:
            self.seating_category = "large"
        
        return self

class QuestionnaireSubmission(BaseModel):
    """Complete questionnaire submission"""
    business_details: BusinessDetails
    submission_timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    session_id: Optional[str] = None
    user_agent: Optional[str] = None
