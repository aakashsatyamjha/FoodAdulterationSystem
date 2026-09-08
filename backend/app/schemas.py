"""
Pydantic Schemas for API Requests and Responses
Food Safety + Adulteration + Risk Assessment + Global Regulatory + Consumer Intelligence
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NutritionInfo(BaseModel):
    energy_kcal: float = 0.0
    sugar_g: float = 0.0
    sodium_mg: float = 0.0
    saturated_fat_g: float = 0.0
    trans_fat_g: float = 0.0
    protein_g: float = 0.0
    fiber_g: float = 0.0

class UserPreferences(BaseModel):
    low_sugar: bool = False
    low_sodium: bool = False
    high_protein: bool = False
    vegetarian: bool = True
    vegan: bool = False
    gluten_free: bool = False
    allergen_safe: bool = False
    low_additives: bool = False
    low_processed: bool = False

class AnalyzeProductRequest(BaseModel):
    product_name: Optional[str] = "Packaged Food"
    brand: Optional[str] = "Generic / Packaged"
    category: Optional[str] = "Packaged Food"
    barcode: Optional[str] = None
    ingredients: str
    nutrition: Optional[NutritionInfo] = None
    scan_type: Optional[str] = "manual"
    selected_country: Optional[str] = "IN"
    user_preferences: Optional[UserPreferences] = None
    custom_thresholds: Optional[Dict[str, float]] = None

class AdulterationIndicator(BaseModel):
    substance: str
    matched_text: str
    hazard_type: str
    severity: str
    reason: str
    confidence: float
    target_category: str

class ConcerningAdditive(BaseModel):
    name: str
    matched_text: str
    type: str
    risk_level: str
    concern: str

class CountryComplianceSummary(BaseModel):
    country_code: str
    country_name: str
    authority: str
    full_authority: str
    framework: str
    flag: str
    verdict: str
    verdict_text: str
    summary: str
    passed_criteria: List[Dict[str, Any]] = []
    conditional_criteria: List[Dict[str, Any]] = []
    failed_criteria: List[Dict[str, Any]] = []
    total_criteria_evaluated: int = 0

class DecisionTraceStep(BaseModel):
    step_num: int
    title: str
    status: str
    detail: str
    icon: str

class FullFoodSafetyReport(BaseModel):
    id: Optional[int] = None
    product_name: str
    brand: str
    barcode: Optional[str] = None
    category: str
    scan_type: str
    quality_score: int
    overall_assessment: str
    final_verdict_badge: str
    final_explanation: str
    safety_disclaimer: str
    risk_level: Optional[str] = None
    
    # 4 Pillars
    adulteration: Dict[str, Any]
    risk: Dict[str, Any]
    regulatory: Dict[str, Any]
    consumer: Dict[str, Any]
    
    # Decision Trace
    decision_trace: Dict[str, Any]
    
    # Raw Ingredients & Nutrition
    matched_ingredients: List[Dict[str, Any]] = []
    parsed_ingredients: List[str] = []
    nutrition: NutritionInfo
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None

class ScanHistoryItem(BaseModel):
    id: int
    product_name: str
    brand: str
    barcode: Optional[str] = None
    category: str
    scan_type: str
    quality_score: int
    risk_level: str
    ingredients: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    history: Optional[List[Dict[str, Any]]] = None

class ConsumerEvaluationRequest(BaseModel):
    ingredients: str
    nutrition: Optional[NutritionInfo] = None
    preferences: Optional[UserPreferences] = None
    custom_thresholds: Optional[Dict[str, float]] = None
