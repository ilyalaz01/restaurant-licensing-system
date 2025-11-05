"""
Report Models
Pydantic models for report data
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ReportSection(BaseModel):
    """Report section model"""
    id: str
    title: str
    priority: str
    content: str
    icon: Optional[str] = None
    action_items: Optional[List[Dict]] = None
    checklist: Optional[List[Dict]] = None
    milestones: Optional[List[Dict]] = None
    breakdown: Optional[Dict[str, int]] = None

class ReportStatistics(BaseModel):
    """Report statistics model"""
    total_requirements: int
    critical_items: int
    estimated_days: int
    estimated_cost: int
    complexity_score: str

class ReportMetadata(BaseModel):
    """Report metadata model"""
    ai_model: str
    regulations_version: str
    report_version: str
    language: str = "en"

class ReportResponse(BaseModel):
    """Complete report response model"""
    report_id: str
    generated_at: str
    business_name: str
    ai_generated: bool
    executive_summary: str
    sections: List[ReportSection]
    statistics: ReportStatistics
    metadata: ReportMetadata
    mock_mode: Optional[bool] = False
