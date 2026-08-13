from typing import Any, Dict, List


class ExecutiveEngine:
    """
    BizMind AI Executive Intelligence Engine.

    Converts insights, decisions, and opportunities into
    prioritized executive-level business actions.
    """

    PRIORITY_ORDER = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    @staticmethod
    def generate_executive_actions(
        insights: List[Dict[str, Any]],
        decision_analysis: Any,
        opportunity_analysis: Any,
    ) -> Dict[str, Any]:

        # -----------------------------------------------------
        # Collect business decisions
        # -----------------------------------------------------

        decisions = getattr(
            decision_analysis,
            "decisions",
            [],
        )

        opportunities = getattr(
            opportunity_analysis,
            "opportunities",
            [],
        )

        # -----------------------------------------------------
        # Find highest-priority decision
        # -----------------------------------------------------

        top_decision = None

        if decisions:
            top_decision = max(
                decisions,
                key=lambda decision: (
                    ExecutiveEngine.PRIORITY_ORDER.get(
                        decision.priority,
                        0,
                    ),
                    getattr(
                        decision,
                        "confidence",
                        0,
                    ),
                ),
            )

        # -----------------------------------------------------
        # Find highest-priority opportunity
        # -----------------------------------------------------

        top_opportunity = None

        if opportunities:
            top_opportunity = max(
                opportunities,
                key=lambda opportunity: (
                    ExecutiveEngine.PRIORITY_ORDER.get(
                        opportunity.priority,
                        0,
                    ),
                    getattr(
                        opportunity,
                        "confidence",
                        0,
                    ),
                ),
            )

        # -----------------------------------------------------
        # Find most severe insight
        # -----------------------------------------------------

        severity_order = {
            "Critical": 4,
            "Warning": 3,
            "Positive": 1,
        }

        top_insight = None

        if insights:
            top_insight = max(
                insights,
                key=lambda insight: severity_order.get(
                    insight.get("severity", ""),
                    0,
                ),
            )

        # -----------------------------------------------------
        # Generate executive action
        # -----------------------------------------------------

        if top_decision is not None:

            executive_action = top_decision.recommendation

            action_reason = top_decision.reasoning

            action_priority = top_decision.priority

        elif top_insight is not None:

            executive_action = top_insight.get(
                "recommendation",
                "Continue monitoring business performance.",
            )

            action_reason = top_insight.get(
                "finding",
                "Business insight requires management attention.",
            )

            action_priority = (
                "HIGH"
                if top_insight.get("severity") == "Critical"
                else "MEDIUM"
            )

        elif top_opportunity is not None:

            executive_action = top_opportunity.recommendation

            action_reason = top_opportunity.reasoning

            action_priority = top_opportunity.priority

        else:

            executive_action = (
                "Continue monitoring KPIs and maintain "
                "current business performance."
            )

            action_reason = (
                "No major business risks or opportunities "
                "were detected."
            )

            action_priority = "LOW"

        # -----------------------------------------------------
        # Executive summary
        # -----------------------------------------------------

        if top_decision is not None:

            executive_summary = (
                f"Management attention should focus on "
                f"{top_decision.title.lower()}."
            )

        elif top_opportunity is not None:

            executive_summary = (
                f"The strongest identified growth opportunity "
                f"is {top_opportunity.title.lower()}."
            )

        else:

            executive_summary = (
                "Business performance is currently stable "
                "with no major priority requiring immediate action."
            )

        # -----------------------------------------------------
        # Return executive intelligence
        # -----------------------------------------------------

        return {
            "top_priority": (
                top_decision.title
                if top_decision is not None
                else (
                    top_insight.get("title")
                    if top_insight is not None
                    else "No Immediate Priority"
                )
            ),
            "priority_level": action_priority,
            "executive_action": executive_action,
            "action_reason": action_reason,
            "executive_summary": executive_summary,
            "top_decision": (
                top_decision.model_dump()
                if top_decision is not None
                else None
            ),
            "top_insight": top_insight,
            "top_opportunity": (
                top_opportunity.model_dump()
                if top_opportunity is not None
                else None
            ),
        }