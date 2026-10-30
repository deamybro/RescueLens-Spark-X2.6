"""
RescueLens Data Models & Schemas
Standardized Humanitarian Emergency Triage Data Structures
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class CitizenDemographics(BaseModel):
    total_people: Optional[int] = Field(default=None, description="Estimated number of affected individuals")
    vulnerable_groups: List[str] = Field(default_factory=list, description="Elderly, infants, pregnant, chronic illness, trapped, etc.")

class LocationClues(BaseModel):
    raw_location_text: str = Field(..., description="Location descriptions or landmarks extracted from text")
    landmarks: List[str] = Field(default_factory=list, description="Key landmarks, street names, intersections")
    gps_coordinates: Optional[str] = Field(default=None, description="Coordinates if present")

class ResourceNeed(BaseModel):
    category: str = Field(..., description="medical | boat_rescue | heavy_extraction | food_water | fuel_power | evacuation_transport")
    urgency: str = Field(..., description="critical | high | medium | low")
    details: str = Field(..., description="Specific details of what is needed")

class EmergencyTriageResult(BaseModel):
    incident_id: str
    priority_level: str = Field(..., description="P1-Immediate (Life-threatening) | P2-Urgent (Severe threat) | P3-Routine (Stabilized/Logistics)")
    urgency_score: int = Field(..., ge=1, le=10, description="Triage score from 1 (lowest) to 10 (most critical)")
    disaster_category: str = Field(..., description="flood, earthquake, wildfire, medical, shelter, infrastructure")
    summary: str = Field(..., description="Crisp one-sentence summary for rapid dispatcher comprehension")
    thinking_process: str = Field(default="", description="The step-by-step reasoning behind the priority decision")
    location: LocationClues
    demographics: CitizenDemographics
    resources_required: List[ResourceNeed]
    hazards_identified: List[str] = Field(default_factory=list, description="Secondary hazards e.g., gas leaks, rising flood, smoke inhalation")
    human_verification_recommended: bool = Field(default=True, description="Human dispatcher sign-off flag")
    human_verification_notes: str = Field(default="", description="Key uncertainty or ambiguity that the dispatcher should check")
