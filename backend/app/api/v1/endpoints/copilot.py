from typing import Optional
from fastapi import APIRouter, Query

from app.schemas.copilot import (
    AuditHistoryResponse,
    CopilotQueryRequest,
    CopilotQueryResponse,
    MultiAgentSynthesisRequest,
    MultiAgentSynthesisResponse,
)
from app.services.copilot.engine import CopilotEngine
from app.services.copilot.orchestrator import MultiAgentOrchestrator
from app.services.copilot.repository import CopilotAuditRepository

router = APIRouter(prefix="/copilot", tags=["AI Business Copilot"])

copilot_engine = CopilotEngine()
orchestrator = MultiAgentOrchestrator()
audit_repo = CopilotAuditRepository()


@router.post(
    "/query",
    response_model=CopilotQueryResponse,
    summary="Query BizMind AI Business Copilot with natural language",
)
def query_copilot(request: CopilotQueryRequest):
    """
    Interactive Business Copilot endpoint.
    Automatically classifies user intent, delegates across analytical engines
    (RiskEngine, ForecastEngine, ScenarioSimulator, MultiAgentOrchestrator),
    synthesizes explainable executive briefings, and logs the interaction for auditability.
    """
    return copilot_engine.process_query(request)


@router.post(
    "/synthesize",
    response_model=MultiAgentSynthesisResponse,
    summary="Synthesize multi-agent executive consensus and debate analysis",
)
def synthesize_multi_agent(request: MultiAgentSynthesisRequest):
    """
    Orchestrates cross-functional domain agents (Finance, Sales, Marketing,
    Risk, Operations), conducts cross-agent consensus debate, resolves
    domain friction, and returns explainable prioritized recommendations.
    """
    return orchestrator.synthesize(request)


@router.get(
    "/history",
    response_model=AuditHistoryResponse,
    summary="Retrieve persistent copilot audit trail and interaction history",
)
def get_audit_history(
    session_id: Optional[str] = Query(None, description="Optional filter by session ID"),
    limit: int = Query(50, ge=1, le=200, description="Maximum records to retrieve"),
):
    """
    Returns historical copilot interactions, query intents, and tool call audit logs from SQLite repository.
    """
    logs = audit_repo.get_history(session_id=session_id, limit=limit)
    return AuditHistoryResponse(total_records=len(logs), history=logs)


@router.delete(
    "/history",
    summary="Clear copilot audit history",
)
def clear_audit_history(
    session_id: Optional[str] = Query(None, description="Optional session ID to clear"),
):
    """
    Clear copilot interaction records from persistent storage.
    """
    cleared = audit_repo.clear_history(session_id=session_id)
    return {
        "status": "success",
        "session_id": session_id or "all",
        "cleared_records": cleared,
    }
