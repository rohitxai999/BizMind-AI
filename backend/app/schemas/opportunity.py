from typing import List

from pydantic import BaseModel, Field


class OpportunityEvidence(BaseModel):
    metric: str
    value: float
    threshold: float
    explanation: str


class BusinessOpportunity(BaseModel):
    title: str
    category: str
    priority: str = Field(
        description="Opportunity priority: LOW, MEDIUM, HIGH, or CRITICAL"
    )
    opportunity: str
    evidence: List[OpportunityEvidence]
    reasoning: str
    recommendation: str
    expected_impact: str
    confidence: float = Field(ge=0.0, le=1.0)


class OpportunityAnalysis(BaseModel):
    opportunities: List[BusinessOpportunity]
    total_opportunities: int
    high_priority_opportunities: int