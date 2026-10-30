from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentPerspective(BaseModel):
    """Domain-specific analysis and recommendations from an individual agent."""

    agent_name: str = Field(..., description="Name of the specialized AI agent")
    domain: str = Field(..., description="Domain area: finance, sales, marketing, risk, or operations")
    sentiment: str = Field(..., description="Bullish, Cautious, Neutral, or Critical")
    priority_score: int = Field(..., ge=0, le=100, description="Urgency/priority score from 0 to 100")
    key_findings: List[str] = Field(default_factory=list, description="Primary domain findings")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Calculated domain KPIs")
    recommendations: List[str] = Field(default_factory=list, description="Domain specific recommendations")


class AgentDebatePoint(BaseModel):
    """Cross-agent friction, tradeoff, or debate point identified across domains."""

    topic: str = Field(..., description="Strategic debate topic or tension point")
    advocating_agents: List[str] = Field(default_factory=list, description="Agents supporting this direction")
    dissenting_agents: List[str] = Field(default_factory=list, description="Agents raising concerns or counter-proposals")
    tension_description: str = Field(..., description="Explanation of the strategic conflict or trade-off")
    resolution: str = Field(..., description="Synthesized executive resolution balancing risk and growth")


class ExplainableRecommendation(BaseModel):
    """Structured, evidence-backed recommendation with explainability metrics."""

    id: str = Field(..., description="Unique recommendation identifier")
    title: str = Field(..., description="Clear, action-oriented title")
    category: str = Field(..., description="Cost Optimization, Revenue Scaling, Risk Mitigation, or Operational Leverage")
    priority: str = Field(..., description="Critical, High, Medium, or Low")
    action_plan: List[str] = Field(default_factory=list, description="Sequential implementation steps")
    rationale: str = Field(..., description="Why this recommendation was generated and prioritized")
    evidence_metrics: Dict[str, Any] = Field(default_factory=dict, description="Exact KPI evidence triggering this action")
    expected_impact: str = Field(..., description="Expected qualitative business outcome")
    quantified_roi_estimate: Optional[str] = Field(None, description="Quantified ROI or profit improvement estimate")
    risk_reduction_potential: int = Field(0, ge=0, le=100, description="Estimated points of risk score reduction")
    timeframe: str = Field(..., description="Immediate (0-30 days), Short-Term (30-90 days), or Long-Term (90+ days)")
    feasibility_score: int = Field(..., ge=0, le=100, description="Execution feasibility score (0-100)")


class MultiAgentSynthesisRequest(BaseModel):
    """Input payload for multi-agent executive intelligence synthesis."""

    business_data: Dict[str, Any] = Field(
        ...,
        description="Core business metrics (revenue, expenses, customers, employees, previous_revenue, etc.)",
    )
    focus_areas: Optional[List[str]] = Field(
        None,
        description="Optional focus areas: ['profitability', 'growth', 'risk', 'efficiency']",
    )
    risk_tolerance: Optional[str] = Field(
        "moderate",
        description="Executive risk tolerance: 'conservative', 'moderate', or 'aggressive'",
    )


class MultiAgentSynthesisResponse(BaseModel):
    """Comprehensive consensus analysis produced by the multi-agent system."""

    consensus_score: int = Field(..., ge=0, le=100, description="Cross-agent alignment index (0-100%)")
    consensus_status: str = Field(..., description="High Alignment, Moderate Alignment, or Strategic Tension Detected")
    perspectives: List[AgentPerspective] = Field(..., description="Individual agent domain analyses")
    debate_points: List[AgentDebatePoint] = Field(default_factory=list, description="Identified cross-domain strategic tradeoffs")
    risk_assessment: Dict[str, Any] = Field(..., description="Standardized RiskEngine assessment with explainable findings")
    executive_consensus_plan: str = Field(..., description="Synthesized executive action plan resolving domain tensions")
    prioritized_recommendations: List[ExplainableRecommendation] = Field(..., description="Actionable, explainable recommendations")


class CopilotQueryRequest(BaseModel):
    """Input query for the interactive AI Business Copilot."""

    query: str = Field(..., min_length=2, description="Natural language business inquiry")
    business_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional current business metrics snapshot (revenue, expenses, customers, employees, etc.)",
    )
    historical_data: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Optional historical time-series data points for forecast-related queries",
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for conversation continuity and audit tracking",
    )


class CopilotQueryResponse(BaseModel):
    """Authoritative, evidence-grounded response from the BizMind AI Copilot."""

    session_id: str = Field(..., description="Session identifier for audit tracking")
    intent: str = Field(..., description="Detected executive intent (e.g. SCENARIO_SIMULATION, FORECAST_INQUIRY, RISK_ANALYSIS, STRATEGIC_PLANNING, PERFORMANCE_DIAGNOSIS)")
    answer: str = Field(..., description="Synthesized executive answer with natural language reasoning")
    data_evidence: Dict[str, Any] = Field(default_factory=dict, description="Computed metrics and quantitative evidence citations")
    recommended_actions: List[str] = Field(default_factory=list, description="Immediate strategic actions")
    suggested_follow_up_queries: List[str] = Field(default_factory=list, description="Relevant questions the leader can ask next")
    tool_invocations: List[str] = Field(default_factory=list, description="Engines and tools executed to answer this query")
    timestamp: str = Field(..., description="ISO 8601 timestamp of query generation")


class AuditLogEntry(BaseModel):
    """Persistent audit record of an executive interaction with BizMind AI."""

    id: str = Field(..., description="Unique record identifier")
    session_id: str = Field(..., description="Session ID")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    query: str = Field(..., description="Original user prompt or action")
    intent: str = Field(..., description="Identified intent")
    summary: str = Field(..., description="Summary of AI analysis and recommendations")
    tools_called: List[str] = Field(default_factory=list, description="Engines and tools invoked")


class AuditHistoryResponse(BaseModel):
    """Collection of past copilot interactions."""

    total_records: int
    history: List[AuditLogEntry]
