from __future__ import annotations
from typing import Dict, List, Optional, TypedDict
from pydantic import BaseModel, Field
from typing import TypedDict, Dict, List

class AstroData_Pydantic(BaseModel):
    chart_summary: str = Field(..., description="High-level chart summary")
    planetary_positions: Dict[str, str] = Field(..., description="Planet→position (sign/house/degree)")
    dashas: Dict[str, str] = Field(..., description="Mahadasha/Antardasha/pratyantar info")
    yogas_doshas: List[str] = Field(default_factory=list, description="Yogas & Doshas present")
    user_question: str = Field(..., description="User's question")


class AstroData_Typed(TypedDict):
    """Structured astrology data returned from the LLM"""
    
    chart_summary: str  # Overall summary of the user's birth chart
    planetary_positions: Dict[str, str]  # Planetary positions like Sun, Moon, Mars etc.
    dashas: Dict[str, str]  # Current Mahadasha, Antardasha and other dasha periods
    yogas_doshas: List[str]  # Important yogas and doshas found in the chart
    user_question: str  # User's question asked to the astrologer


class IntentSpec_Pydantic(BaseModel):
    topic: str = Field(..., description="Main area: career/marriage/health/finance/spirituality/other")
    timeframe: Optional[str] = Field(None, description="Explicit time window, if any")
    focus_houses: List[str] = Field(default_factory=list, description="Houses to consider (e.g., ['10th','6th'])")
    focus_planets: List[str] = Field(default_factory=list, description="Planets to consider")
    relevant_dasha: Optional[str] = Field(None, description="Mahadasha/Antardasha to focus on if implied")

class IntentSpec_Typed(TypedDict, total=False):
    """User's intent specification for astrology question"""
    
    topic: str  # Main area: career/marriage/health/finance/spirituality/other
    timeframe: Optional[str]  # Explicit time window, if any
    focus_houses: List[str]  # Houses to consider (e.g., ['10th','6th'])
    focus_planets: List[str]  # Planets to consider
    relevant_dasha: Optional[str]  # Mahadasha/Antardasha to focus on if implied



