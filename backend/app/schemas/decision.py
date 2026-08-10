from typing import List, Optional

from pydantic import BaseModel, Field


class DecisionEvidence(BaseModel):
    metric: str
    value: float
    comparison: Optional[float] = None
    explanation: str


class BusinessDecision(BaseModel):
    title: str
    category: str
    priority: str = Field(
        description="Decision priority: LOW, MEDIUM, HIGH, or CRITICAL"
    )
    problem: str
    evidence: List[DecisionEvidence]
    reasoning: str
    recommendation: str
    expected_impact: str
    risk_level: str
    confidence: float = Field(ge=0.0, le=1.0)


class DecisionAnalysis(BaseModel):
    decisions: List[BusinessDecision]
    total_decisions: int
    critical_decisions: int
    high_priority_decisions: int