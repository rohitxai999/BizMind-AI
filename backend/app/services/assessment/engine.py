from typing import Any, Dict, List


class UnifiedAssessmentEngine:
    """
    Combines Insights Engine and multi-agent results
    into a single executive-level business assessment.
    """

    @staticmethod
    def generate_assessment(
        insights: Dict[str, Any],
        agent_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:

        key_strengths: List[str] = []
        key_risks: List[str] = []
        key_opportunities: List[str] = []

        # =========================================================
        # Analyze AI Insights
        # =========================================================

        for insight in insights.get("insights", []):

            severity = insight.get("severity", "")
            title = insight.get("title", "")
            recommendation = insight.get(
                "recommendation",
                ""
            )

            if severity == "Positive":
                key_strengths.append(title)

            elif severity in {"Warning", "Critical"}:
                key_risks.append(title)

                if recommendation:
                    key_opportunities.append(
                        recommendation
                    )

        # =========================================================
        # Analyze Agent Results
        # =========================================================

        agent_results = agent_analysis.get(
            "results",
            []
        )

        agent_risks: List[str] = []

        for result in agent_results:

            if result.get("status") != "success":
                continue

            agent_name = result.get(
                "agent",
                "Unknown Agent"
            )

            # Finance
            if agent_name == "Finance Agent":

                financial_health = result.get(
                    "financial_health"
                )

                if financial_health == "Healthy":
                    key_strengths.append(
                        "Finance Agent reports healthy profitability."
                    )

                elif financial_health == "Loss":
                    agent_risks.append(
                        "Finance Agent reports a business loss."
                    )

            # Sales
            elif agent_name == "Sales Agent":

                performance = result.get(
                    "performance"
                )

                if performance in {
                    "Excellent",
                    "Good"
                }:
                    key_strengths.append(
                        f"Sales performance is {performance.lower()}."
                    )

                elif performance == "Poor":
                    agent_risks.append(
                        "Sales performance requires improvement."
                    )

            # Marketing
            elif agent_name == "Marketing Agent":

                marketing_status = result.get(
                    "marketing_status"
                )

                if marketing_status in {
                    "Excellent Growth",
                    "Growing"
                }:
                    key_strengths.append(
                        f"Marketing status: {marketing_status}."
                    )

                elif marketing_status == "Needs Improvement":
                    agent_risks.append(
                        "Marketing performance needs improvement."
                    )

            # Risk
            elif agent_name == "Risk Agent":

                risk_level = result.get(
                    "risk_level"
                )

                if risk_level == "High":
                    agent_risks.append(
                        "Risk Agent identified high business risk."
                    )

                elif risk_level == "Medium":
                    agent_risks.append(
                        "Risk Agent identified medium business risk."
                    )

        # =========================================================
        # Merge Agent Risks
        # =========================================================

        key_risks.extend(agent_risks)

        # =========================================================
        # Remove Duplicates
        # =========================================================

        key_strengths = list(
            dict.fromkeys(key_strengths)
        )

        key_risks = list(
            dict.fromkeys(key_risks)
        )

        key_opportunities = list(
            dict.fromkeys(key_opportunities)
        )

        # =========================================================
        # Determine Overall Risk
        # =========================================================

        insight_risk = insights.get(
            "risk_level",
            "Medium"
        )

        risk_levels = []

        if insight_risk == "High":
            risk_levels.append(3)
        elif insight_risk == "Medium":
            risk_levels.append(2)
        else:
            risk_levels.append(1)

        for result in agent_results:

            if result.get("agent") != "Risk Agent":
                continue

            risk_level = result.get(
                "risk_level",
                "Medium"
            )

            if risk_level == "High":
                risk_levels.append(3)

            elif risk_level == "Medium":
                risk_levels.append(2)

            else:
                risk_levels.append(1)

        average_risk = (
            sum(risk_levels) / len(risk_levels)
            if risk_levels
            else 2
        )

        if average_risk >= 2.5:
            overall_risk = "High"
        elif average_risk >= 1.5:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"

        # =========================================================
        # Overall Status
        # =========================================================

        health_score = insights.get(
            "health_score",
            0
        )

        if health_score >= 85:
            overall_status = "Excellent"
        elif health_score >= 70:
            overall_status = "Strong"
        elif health_score >= 50:
            overall_status = "Moderate"
        else:
            overall_status = "Weak"

        # =========================================================
        # Confidence Score
        # =========================================================

        successful_agents = sum(
            1
            for result in agent_results
            if result.get("status") == "success"
        )

        total_agents = len(agent_results)

        agent_confidence = (
            successful_agents / total_agents
            if total_agents > 0
            else 0
        )

        confidence = round(
            (
                (health_score / 100) * 0.6
                + agent_confidence * 0.4
            ),
            2
        )

        # =========================================================
        # Executive Summary
        # =========================================================

        executive_summary = (
            f"Overall business status is "
            f"{overall_status.lower()} with "
            f"{overall_risk.lower()} risk. "
            f"BizMind analyzed the business using "
            f"the KPI intelligence engine and "
            f"{successful_agents} successful AI agents."
        )

        # =========================================================
        # Final Assessment
        # =========================================================

        return {
            "overall_status": overall_status,
            "overall_risk": overall_risk,
            "confidence": confidence,
            "health_score": health_score,
            "key_strengths": key_strengths,
            "key_risks": key_risks,
            "key_opportunities": key_opportunities,
            "executive_summary": executive_summary,
        }