from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from enum import Enum
from pydantic import BaseModel, Field

class KnowledgeLevel(str, Enum):
    BEGINNER = "Iniciante"
    INTERMEDIATE = "Intermediário"
    ADVANCED = "Avançado"

class AllocationData(BaseModel):
    name: str = Field(...)
    value: float = Field(...)

class EvolutionData(BaseModel):
    year: int = Field(...)
    value: float = Field(...)

class ReportCharts(BaseModel):
    allocation_pie: List[AllocationData] = Field(...)
    evolution_bar: List[EvolutionData] = Field(...)

class FinalReport(BaseModel):
    markdown_text: str = Field(...)
    charts: ReportCharts = Field(...)

class AssetPreferences(BaseModel):
    accepts_public_titles: bool = Field(default=True)
    accepts_private_titles: bool = Field(default=True)
    accepts_national: bool = Field(default=True)
    accepts_international: bool = Field(default=False)
    accepted_asset_types: List[str] = Field(default_factory=list)

class ClientData(BaseModel):
    name: str = Field(...)
    age: int = Field(..., ge=0)
    knowledge_level: KnowledgeLevel = Field(...)
    has_invested_before: bool = Field(...)
    past_investments: Optional[str] = Field(None)
    
    investment_horizon_months: int = Field(..., ge=6, le=420)
    monthly_income: float = Field(..., ge=0)
    monthly_contribution: float = Field(..., ge=0)
    initial_investment: float = Field(..., ge=0)
    
    asset_preferences: Optional[AssetPreferences] = Field(None)
    additional_comments: Optional[str] = Field(None)

class AgentState(TypedDict):
    raw_input: Dict[str, Any]
    standardized_client_data: Optional[ClientData]
    matched_products: List[Dict[str, Any]]
    draft_report: Optional[FinalReport]
    final_report: Optional[FinalReport]
    status_code: int
    retry_count: int
    is_blacklisted: bool
    blacklist_reason: Optional[str]
    demographic_category: str
    financial_health_warning: bool
    math_operations_log: List[str]
    audit_logs: Annotated[List[str], operator.add]