import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.schemas.copilot import (
    CopilotQueryRequest,
    CopilotQueryResponse,
    MultiAgentSynthesisRequest,
)
from app.schemas.forecast import ForecastRequest, HistoricalDataPoint
from app.schemas.scenario import (
    BaselineBusinessInput,
    ScenarioLevers,
    ScenarioSimulationInput,
)
from app.services.copilot.orchestrator import MultiAgentOrchestrator
from app.services.copilot.repository import CopilotAuditRepository
from app.services.forecast.engine import ForecastEngine
from app.services.insights_engine import InsightsEngine
from app.services.risk.engine import RiskEngine
from app.services.simulator.engine import ScenarioSimulatorEngine


class CopilotEngine:
    """
    BizMind AI Autonomous Business Copilot Engine.

    Empowers leadership to query business health, simulate what-if scenarios,
    evaluate time-series predictive forecasts, investigate risk drivers, and
    obtain explainable multi-agent strategic consensus with natural language reasoning.
    """

    DEFAULT_BUSINESS_DATA = {
        "revenue": 250000.0,
        "expenses": 170000.0,
        "profit": 80000.0,
        "previous_revenue": 220000.0,
        "previous_expenses": 160000.0,
        "customers": 150,
        "employees": 12,
        "revenue_growth": 13.64,
        "expense_growth": 6.25,
    }

    DEFAULT_HISTORICAL_DATA = [
        {"period": "2026-01", "revenue": 190000.0, "expenses": 145000.0, "customers": 110},
        {"period": "2026-02", "revenue": 205000.0, "expenses": 150000.0, "customers": 122},
        {"period": "2026-03", "revenue": 220000.0, "expenses": 160000.0, "customers": 135},
        {"period": "2026-04", "revenue": 250000.0, "expenses": 170000.0, "customers": 150},
    ]

    def __init__(self, repository: Optional[CopilotAuditRepository] = None):
        self.repository = repository or CopilotAuditRepository()
        self.orchestrator = MultiAgentOrchestrator()
        self.forecast_engine = ForecastEngine()
        self.simulator = ScenarioSimulatorEngine()


    @staticmethod
    def classify_intent(query: str) -> str:
        """
        Classify executive query into one of five core analytical intents:
        - SCENARIO_SIMULATION
        - FORECAST_INQUIRY
        - RISK_ANALYSIS
        - STRATEGIC_PLANNING
        - PERFORMANCE_DIAGNOSIS
        """
        q = query.lower()

        # 1. Scenario Simulation
        scenario_keywords = ["what if", "simulate", "simulation", "scenario", "stress test", "drop by", "increase by", "recession"]
        if any(kw in q for kw in scenario_keywords):
            return "SCENARIO_SIMULATION"

        # 2. Forecasting & Predictive Analytics
        forecast_keywords = ["forecast", "predict", "future", "next quarter", "next month", "trend", "trajectory", "run rate", "extrapolate"]
        if any(kw in q for kw in forecast_keywords):
            return "FORECAST_INQUIRY"

        # 3. Risk Analysis
        risk_keywords = ["risk", "danger", "vulnerability", "risk score", "exposure", "threat", "mitigate", "mitigation", "safe"]
        if any(kw in q for kw in risk_keywords):
            return "RISK_ANALYSIS"

        # 4. Strategic Recommendations & Multi-Agent Planning
        strategy_keywords = ["strategy", "recommend", "recommendation", "plan", "how to improve", "action plan", "what should we do", "roadmap", "grow", "scale"]
        if any(kw in q for kw in strategy_keywords):
            return "STRATEGIC_PLANNING"

        # 5. Default / Performance Diagnosis
        return "PERFORMANCE_DIAGNOSIS"

    def _extract_scenario_levers(self, query: str) -> ScenarioLevers:
        """Extract scenario parameters from natural language or return default stress test."""
        q = query.lower()
        rev_change = 0.0
        exp_change = 0.0

        # Try to extract percentages without cross-clause bleeding
        rev_drop_match = re.search(r"revenue(?:(?!expenses?).)*?(?:drops?|declines?|falls?|decreases?|down)\s*(?:by)?\s*(\d+)%", q)
        rev_up_match = re.search(r"revenue(?:(?!expenses?).)*?(?:grows?|increases?|rises?|up)\s*(?:by)?\s*(\d+)%", q)
        if rev_drop_match:
            rev_change = -float(rev_drop_match.group(1))
        elif rev_up_match:
            rev_change = float(rev_up_match.group(1))

        exp_up_match = re.search(r"expenses?(?:(?!revenue).)*?(?:grows?|increases?|rises?|up)\s*(?:by)?\s*(\d+)%", q)
        exp_drop_match = re.search(r"expenses?(?:(?!revenue).)*?(?:drops?|cuts?|declines?|falls?|decreases?|down)\s*(?:by)?\s*(\d+)%", q)
        if exp_up_match:
            exp_change = float(exp_up_match.group(1))
        elif exp_drop_match:
            exp_change = -float(exp_drop_match.group(1))


        if rev_change == 0.0 and exp_change == 0.0:
            # Default to severe stress test if user asked for general stress test
            rev_change = -15.0
            exp_change = 5.0
            name = "Simulated Market Contraction"
            desc = "Automated stress scenario modeling 15% revenue decline and 5% operational cost inflation."
        else:
            name = f"Custom Simulation (Rev {rev_change:+.1f}%, Exp {exp_change:+.1f}%)"
            desc = f"What-if simulation modeling {rev_change:+.1f}% revenue variance and {exp_change:+.1f}% expense variance."

        return ScenarioLevers(
            scenario_name=name,
            revenue_change_pct=rev_change,
            expense_change_pct=exp_change,
            customer_change_pct=rev_change * 0.8,
            employee_change=0,
            description=desc,
        )

    def process_query(self, request: CopilotQueryRequest) -> CopilotQueryResponse:
        """
        Main query processing pipeline:
        1. Classifies user intent.
        2. Routes to relevant specialized AI/BI engines.
        3. Synthesizes an executive brief with concrete data citations.
        4. Logs the interaction in the persistent audit repository.
        """
        session_id = request.session_id or str(uuid.uuid4())
        intent = self.classify_intent(request.query)
        data = {**self.DEFAULT_BUSINESS_DATA, **(request.business_data or {})}
        now_iso = datetime.now(timezone.utc).isoformat()

        tool_invocations: List[str] = []
        data_evidence: Dict[str, Any] = {}
        recommended_actions: List[str] = []
        suggested_follow_ups: List[str] = []

        if intent == "SCENARIO_SIMULATION":
            tool_invocations.append("ScenarioSimulatorEngine.simulate")
            tool_invocations.append("RiskEngine.calculate")
            levers = self._extract_scenario_levers(request.query)

            baseline = BaselineBusinessInput(
                revenue=data["revenue"],
                expenses=data["expenses"],
                customers=int(data.get("customers", 100)),
                employees=int(data.get("employees", 10)),
                previous_revenue=float(data.get("previous_revenue", 0)),
                previous_expenses=float(data.get("previous_expenses", 0)),
            )
            sim_result = self.simulator.simulate(baseline, levers)


            data_evidence = {
                "scenario_name": sim_result.scenario_name,
                "projected_revenue": sim_result.projected_financials.revenue,
                "projected_expenses": sim_result.projected_financials.expenses,
                "projected_profit": sim_result.projected_financials.profit,
                "projected_profit_margin": sim_result.projected_financials.profit_margin,
                "baseline_risk_score": sim_result.baseline_risk_score,
                "projected_risk_score": sim_result.projected_risk_score,
                "risk_delta": sim_result.risk_delta,
                "risk_trajectory": sim_result.risk_trajectory,
                "strategic_feasibility": sim_result.strategic_feasibility,
            }

            answer = (
                f"### 🔬 What-If Simulation: {sim_result.scenario_name}\n\n"
                f"{sim_result.executive_impact_summary}\n\n"
                f"- **Projected Financials**: Revenue: **${sim_result.projected_financials.revenue:,.2f}** | "
                f"Expenses: **${sim_result.projected_financials.expenses:,.2f}** | "
                f"Profit: **${sim_result.projected_financials.profit:,.2f}** ({sim_result.projected_financials.profit_margin:.1f}% Margin)\n"
                f"- **Risk Trajectory**: {sim_result.risk_trajectory} (Risk score changes from "
                f"**{sim_result.baseline_risk_score}** to **{sim_result.projected_risk_score}**, Δ{sim_result.risk_delta:+d} pts)\n"
                f"- **Feasibility**: **{sim_result.strategic_feasibility}**"
            )
            recommended_actions = [
                f"Simulate compensating cost adjustments to offset {levers.revenue_change_pct:+.1f}% revenue shift.",
                "Review working capital reserves to ensure sufficient liquidity under this trajectory.",
                "Establish early-warning trigger indicators for top client accounts.",
            ]
            suggested_follow_ups = [
                "What happens if we reduce expenses by 10% alongside this drop?",
                "Run a multi-scenario comparison to find the optimal response.",
                "What is our projected risk score under a 20% growth scenario?",
            ]

        elif intent == "FORECAST_INQUIRY":
            tool_invocations.append("ForecastEngine.predict")
            tool_invocations.append("RiskEngine.calculate")

            hist_raw = request.historical_data or self.DEFAULT_HISTORICAL_DATA
            hist_points = [
                HistoricalDataPoint(
                    period=str(h["period"]),
                    revenue=float(h["revenue"]),
                    expenses=float(h["expenses"]),
                    profit=float(h.get("profit", float(h["revenue"]) - float(h["expenses"]))),
                    customers=int(h.get("customers", 0)),
                )
                for h in hist_raw
            ]

            forecast_res = self.forecast_engine.predict(
                ForecastRequest(historical_data=hist_points, forecast_periods=3, confidence_level=0.90)
            )

            next_period = forecast_res.forecasted_periods[0]
            data_evidence = {
                "forecast_horizon": forecast_res.forecast_horizon,
                "projected_annual_run_rate": forecast_res.projected_annual_run_rate,
                "future_risk_trajectory": forecast_res.projected_future_risk_trajectory,
                "confidence_score": forecast_res.confidence_score,
                "next_period_revenue_prediction": next_period.predicted_revenue,
                "next_period_revenue_lower_bound": next_period.revenue_lower_bound,
                "next_period_revenue_upper_bound": next_period.revenue_upper_bound,
                "next_period_projected_risk": next_period.projected_risk_score,
                "trend_direction": forecast_res.trend_analysis.revenue_trend_direction,
            }

            answer = (
                f"### 📈 Predictive Forecast & Trajectory Analysis\n\n"
                f"{forecast_res.executive_takeaway}\n\n"
                f"- **Forward Momentum**: Revenue trend is **{forecast_res.trend_analysis.revenue_trend_direction}** "
                f"with an average periodic growth rate of **{forecast_res.trend_analysis.avg_period_growth_rate:+.2f}%**.\n"
                f"- **Next Period Projection ({next_period.period})**: Expected Revenue: **${next_period.predicted_revenue:,.2f}** "
                f"(90% Confidence Interval: ${next_period.revenue_lower_bound:,.2f} - ${next_period.revenue_upper_bound:,.2f}).\n"
                f"- **Annual Run-Rate**: Projected at **${forecast_res.projected_annual_run_rate:,.2f}** with "
                f"a **{forecast_res.projected_future_risk_trajectory}** future risk trajectory."
            )
            recommended_actions = [
                "Track actual revenue against the predicted 90% confidence lower bound.",
                "Align operating expense growth with projected revenue momentum.",
                "Review any detected historical anomalies to prevent recurring variance.",
            ]
            suggested_follow_ups = [
                "What is our current business risk score?",
                "What if revenue drops by 10% next quarter?",
                "Show cross-agent strategic recommendations to boost growth.",
            ]

        elif intent == "RISK_ANALYSIS":
            tool_invocations.append("RiskEngine.calculate")
            risk_res = RiskEngine.calculate(
                {
                    "revenue": data["revenue"],
                    "expenses": data["expenses"],
                    "profit": data["profit"],
                    "revenue_growth": data.get("revenue_growth", 0.0),
                }
            )

            data_evidence = {
                "risk_score": risk_res["risk_score"],
                "risk_level": risk_res["risk_level"],
                "profit_margin": risk_res["profit_margin"],
                "expense_ratio": risk_res["expense_ratio"],
                "risk_factors_count": len(risk_res.get("risk_factors", [])),
                "risk_findings": risk_res.get("risk_findings", []),
            }

            findings_text = ""
            if risk_res.get("risk_findings"):
                findings_text = "\n" + "\n".join(
                    [f"- **{f['factor']}**: {f['explanation']} *(Severity: {f['severity']} | Mitigation: {f['mitigation']})*" for f in risk_res["risk_findings"]]
                )

            answer = (
                f"### 🛡️ Centralized Risk Assessment & Explainability\n\n"
                f"The business currently registers a **{risk_res['risk_level']}** risk profile with an overall "
                f"Risk Score of **{risk_res['risk_score']}/100**.\n\n"
                f"- **Key Metrics**: Profit Margin: **{risk_res['profit_margin']:.1f}%** | "
                f"Expense Ratio: **{risk_res['expense_ratio']:.1f}%** | "
                f"Revenue Growth: **{risk_res['revenue_growth']:+.1f}%**\n"
                f"- **Risk Drivers**: {risk_res['risk_explanation']}"
                f"{findings_text}"
            )
            recommended_actions = list(risk_res.get("mitigation_recommendations", [])) or [
                "Maintain continuous monitoring of cash flow and expense ratios.",
                "Audit high-value vendor commitments.",
            ]
            suggested_follow_ups = [
                "How can we simulate reducing our expense ratio below 60%?",
                "What do the specialized agents recommend to lower our risk score?",
                "What is our revenue forecast for the next 3 months?",
            ]

        elif intent == "STRATEGIC_PLANNING":
            tool_invocations.append("MultiAgentOrchestrator.synthesize")
            tool_invocations.append("RiskEngine.calculate")

            synthesis_res = self.orchestrator.synthesize(
                MultiAgentSynthesisRequest(business_data=data)
            )

            top_rec = synthesis_res.prioritized_recommendations[0]
            data_evidence = {
                "consensus_score": synthesis_res.consensus_score,
                "consensus_status": synthesis_res.consensus_status,
                "total_perspectives": len(synthesis_res.perspectives),
                "total_debate_points": len(synthesis_res.debate_points),
                "top_recommendation": top_rec.title,
                "top_recommendation_roi": top_rec.quantified_roi_estimate,
            }

            debate_summary = "\n".join(
                [f"- **{d.topic}**: {d.resolution}" for d in synthesis_res.debate_points[:2]]
            )

            answer = (
                f"### 🧭 Multi-Agent Strategic Intelligence & Consensus Plan\n\n"
                f"{synthesis_res.executive_consensus_plan}\n\n"
                f"#### ⚖️ Cross-Domain Debate & Resolutions:\n{debate_summary}\n\n"
                f"#### 🎯 Top Actionable Recommendation:\n"
                f"**{top_rec.title}** ({top_rec.priority} Priority)\n"
                f"- **Why**: {top_rec.rationale}\n"
                f"- **Expected ROI**: {top_rec.quantified_roi_estimate}\n"
                f"- **Risk Reduction**: {top_rec.risk_reduction_potential} pts\n"
                f"- **Timeframe**: {top_rec.timeframe}"
            )
            recommended_actions = [
                rec.title for rec in synthesis_res.prioritized_recommendations[:3]
            ]
            suggested_follow_ups = [
                f"Simulate impact of implementing {top_rec.title}",
                "How does each specialized agent view our current performance?",
                "What happens to our risk score if we execute cost optimization?",
            ]

        else:  # PERFORMANCE_DIAGNOSIS
            tool_invocations.append("InsightsEngine.generate_insights")
            tool_invocations.append("RiskEngine.calculate")

            insights = InsightsEngine.generate_insights(
                revenue=data["revenue"],
                expenses=data["expenses"],
                previous_revenue=float(data.get("previous_revenue", 0)),
                customers=int(data.get("customers", 0)),
                employees=int(data.get("employees", 0)),
                previous_expenses=float(data.get("previous_expenses", 0)),
            )

            data_evidence = {
                "health_score": insights["health_score"],
                "risk_score": insights["risk_score"],
                "risk_level": insights["risk_level"],
                "profit": insights["profit"],
                "profit_margin": insights["profit_margin"],
                "performance_status": insights["performance_status"],
                "executive_summary": insights["executive_summary"],
            }

            answer = (
                f"### 📊 360° Executive Business Performance Diagnosis\n\n"
                f"{insights['executive_summary']}\n\n"
                f"- **Financial Health**: Health Score: **{insights['health_score']}/100** | "
                f"Risk Level: **{insights['risk_level']}** ({insights['risk_score']}/100)\n"
                f"- **Operating Performance**: Revenue: **${insights['revenue']:,.2f}** | "
                f"Profit: **${insights['profit']:,.2f}** ({insights['profit_margin']:.1f}% Margin)\n"
                f"- **Unit Metrics**: ARPU: **${insights['customer_value']:,.2f}** | "
                f"Revenue/Employee: **${insights['revenue_per_employee']:,.2f}**"
            )
            recommended_actions = insights.get("recommendations", [])[:3] or [
                "Continue tracking operational performance against monthly benchmarks.",
            ]
            suggested_follow_ups = [
                "What is our financial risk breakdown?",
                "Can you forecast our revenue for the next quarter?",
                "What if revenue drops by 15% due to market conditions?",
            ]

        # Persist interaction into audit repository
        self.repository.save_interaction(
            session_id=session_id,
            query=request.query,
            intent=intent,
            summary=answer[:250] + "...",
            tools_called=tool_invocations,
        )

        return CopilotQueryResponse(
            session_id=session_id,
            intent=intent,
            answer=answer,
            data_evidence=data_evidence,
            recommended_actions=recommended_actions,
            suggested_follow_up_queries=suggested_follow_ups,
            tool_invocations=tool_invocations,
            timestamp=now_iso,
        )
