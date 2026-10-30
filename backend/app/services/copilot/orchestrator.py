import uuid
from typing import Any, Dict, List, Optional

from app.schemas.copilot import (
    AgentDebatePoint,
    AgentPerspective,
    ExplainableRecommendation,
    MultiAgentSynthesisRequest,
    MultiAgentSynthesisResponse,
)
from app.services.risk.engine import RiskEngine


class MultiAgentOrchestrator:
    """
    BizMind AI Multi-Agent Orchestrator.

    Coordinates specialized domain agents (Finance, Sales, Marketing,
    Risk, Operations), conducts cross-agent consensus debate, resolves
    domain friction, and generates explainable, prioritized recommendations.
    """

    def __init__(self):
        pass

    def _analyze_finance(self, data: Dict[str, Any]) -> AgentPerspective:
        revenue = float(data.get("revenue", 0))
        expenses = float(data.get("expenses", 0))
        profit = float(data.get("profit", revenue - expenses))
        prev_rev = float(data.get("previous_revenue", 0))

        profit_margin = (profit / revenue * 100.0) if revenue > 0 else 0.0
        expense_ratio = (expenses / revenue * 100.0) if revenue > 0 else 100.0
        rev_growth = ((revenue - prev_rev) / prev_rev * 100.0) if prev_rev > 0 else 0.0

        findings = []
        recommendations = []
        metrics = {
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "revenue_growth": round(rev_growth, 2),
        }

        if profit_margin >= 25.0:
            sentiment = "Bullish"
            priority_score = 30
            findings.append(f"Strong profit margin of {profit_margin:.1f}% indicates healthy unit economics.")
            recommendations.append("Reinvest excess cash reserves into high-return growth channels.")
        elif profit_margin >= 10.0:
            sentiment = "Cautious"
            priority_score = 60
            findings.append(f"Moderate profit margin of {profit_margin:.1f}%; operating buffer is acceptable but vulnerable to shocks.")
            recommendations.append("Audit discretionary operating expenses to push margin toward 20%.")
        else:
            sentiment = "Critical"
            priority_score = 90
            findings.append(f"Compressed profit margin ({profit_margin:.1f}%) and high expense ratio ({expense_ratio:.1f}%).")
            recommendations.append("Immediate operating expense reduction and supplier renegotiation required.")

        return AgentPerspective(
            agent_name="Finance Intelligence Agent",
            domain="finance",
            sentiment=sentiment,
            priority_score=priority_score,
            key_findings=findings,
            metrics=metrics,
            recommendations=recommendations,
        )

    def _analyze_sales(self, data: Dict[str, Any]) -> AgentPerspective:
        revenue = float(data.get("revenue", 0))
        customers = int(data.get("customers", 0))
        prev_rev = float(data.get("previous_revenue", 0))

        revenue_per_customer = (revenue / customers) if customers > 0 else 0.0
        rev_growth = ((revenue - prev_rev) / prev_rev * 100.0) if prev_rev > 0 else 0.0

        findings = []
        recommendations = []
        metrics = {
            "customers": customers,
            "revenue_per_customer": round(revenue_per_customer, 2),
            "revenue_growth": round(rev_growth, 2),
        }

        if revenue_per_customer >= 500.0:
            sentiment = "Bullish"
            priority_score = 35
            findings.append(f"High customer value (${revenue_per_customer:.2f} ARPU) demonstrates strong product-market fit.")
            recommendations.append("Target enterprise tier accounts to maximize deal velocity and lifetime value.")
        elif revenue_per_customer >= 200.0:
            sentiment = "Neutral"
            priority_score = 55
            findings.append(f"Moderate customer monetization (${revenue_per_customer:.2f} ARPU).")
            recommendations.append("Introduce premium cross-selling bundles to expand average contract value.")
        else:
            sentiment = "Cautious"
            priority_score = 75
            findings.append(f"Low monetization per customer (${revenue_per_customer:.2f}); acquisition may not offset service costs.")
            recommendations.append("Restructure pricing tiers and evaluate minimum commitment contracts.")

        return AgentPerspective(
            agent_name="Sales Intelligence Agent",
            domain="sales",
            sentiment=sentiment,
            priority_score=priority_score,
            key_findings=findings,
            metrics=metrics,
            recommendations=recommendations,
        )

    def _analyze_marketing(self, data: Dict[str, Any]) -> AgentPerspective:
        customers = int(data.get("customers", 0))
        revenue = float(data.get("revenue", 0))
        prev_rev = float(data.get("previous_revenue", 0))
        rev_growth = ((revenue - prev_rev) / prev_rev * 100.0) if prev_rev > 0 else 0.0

        findings = []
        recommendations = []
        metrics = {
            "customer_base": customers,
            "estimated_market_penetration": "Expanding" if customers >= 500 else "Early Stage",
        }

        if customers >= 1000:
            sentiment = "Bullish"
            priority_score = 25
            findings.append(f"Robust customer base ({customers:,} accounts) provides significant organic referral leverage.")
            recommendations.append("Launch customer advocacy programs and lookalike audience campaigns.")
        elif customers >= 250:
            sentiment = "Neutral"
            priority_score = 50
            findings.append(f"Active base of {customers:,} customers; acquisition pipeline is functional but needs scaling.")
            recommendations.append("Double down on highest-converting acquisition channels and optimize landing page funnel.")
        else:
            sentiment = "Cautious"
            priority_score = 70
            findings.append(f"Limited customer footprint ({customers:,} accounts); high exposure to individual account churn.")
            recommendations.append("Ramp up inbound content marketing and outbound lead generation campaigns.")

        return AgentPerspective(
            agent_name="Marketing Intelligence Agent",
            domain="marketing",
            sentiment=sentiment,
            priority_score=priority_score,
            key_findings=findings,
            metrics=metrics,
            recommendations=recommendations,
        )

    def _analyze_risk(self, data: Dict[str, Any]) -> tuple[AgentPerspective, Dict[str, Any]]:
        risk_input = {
            "revenue": float(data.get("revenue", 0)),
            "expenses": float(data.get("expenses", 0)),
            "profit": float(data.get("profit", float(data.get("revenue", 0)) - float(data.get("expenses", 0)))),
            "revenue_growth": float(data.get("revenue_growth", 0)),
        }
        risk_res = RiskEngine.calculate(risk_input)

        risk_score = risk_res["risk_score"]
        risk_level = risk_res["risk_level"]
        findings = [f"Overall Risk Score: {risk_score}/100 ({risk_level} Risk)."]
        for f in risk_res.get("risk_findings", []):
            findings.append(f"{f['factor']}: {f['explanation']} (Threshold: {f['threshold']})")

        recommendations = list(risk_res.get("mitigation_recommendations", []))
        if not recommendations:
            recommendations.append("Maintain continuous monitoring of cash flow and expense trends.")

        if risk_level == "Low":
            sentiment = "Bullish"
            priority_score = 20
        elif risk_level == "Medium":
            sentiment = "Cautious"
            priority_score = 50
        elif risk_level == "High":
            sentiment = "Critical"
            priority_score = 80
        else:
            sentiment = "Critical"
            priority_score = 95

        perspective = AgentPerspective(
            agent_name="Risk & Compliance Agent",
            domain="risk",
            sentiment=sentiment,
            priority_score=priority_score,
            key_findings=findings,
            metrics={
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_factors_count": len(risk_res.get("risk_factors", [])),
            },
            recommendations=recommendations,
        )
        return perspective, risk_res

    def _analyze_operations(self, data: Dict[str, Any]) -> AgentPerspective:
        revenue = float(data.get("revenue", 0))
        employees = int(data.get("employees", 0))
        expenses = float(data.get("expenses", 0))

        rev_per_emp = (revenue / employees) if employees > 0 else 0.0
        cost_per_emp = (expenses / employees) if employees > 0 else 0.0

        findings = []
        recommendations = []
        metrics = {
            "employees": employees,
            "revenue_per_employee": round(rev_per_emp, 2),
            "cost_per_employee": round(cost_per_emp, 2),
        }

        if rev_per_emp >= 25000.0 or employees == 0:
            sentiment = "Bullish"
            priority_score = 30
            findings.append(f"High workforce productivity (${rev_per_emp:,.2f} revenue/employee).")
            recommendations.append("Capacity is well utilized; selective hiring in key engineering/sales roles is feasible.")
        elif rev_per_emp >= 12000.0:
            sentiment = "Neutral"
            priority_score = 50
            findings.append(f"Balanced operational productivity (${rev_per_emp:,.2f} revenue/employee).")
            recommendations.append("Implement automated tooling before approving additional operational headcount.")
        else:
            sentiment = "Cautious"
            priority_score = 75
            findings.append(f"Low workforce revenue leverage (${rev_per_emp:,.2f} revenue/employee); overhead may outpace output.")
            recommendations.append("Review organizational design and streamline cross-functional workflows.")

        return AgentPerspective(
            agent_name="Operations & Strategy Agent",
            domain="operations",
            sentiment=sentiment,
            priority_score=priority_score,
            key_findings=findings,
            metrics=metrics,
            recommendations=recommendations,
        )

    def _conduct_debate(
        self, perspectives: List[AgentPerspective], risk_data: Dict[str, Any]
    ) -> List[AgentDebatePoint]:
        debate_points: List[AgentDebatePoint] = []
        risk_score = risk_data.get("risk_score", 0)

        # 1. Growth vs Capital Preservation Tradeoff
        fin_p = next((p for p in perspectives if p.domain == "finance"), None)
        risk_p = next((p for p in perspectives if p.domain == "risk"), None)
        sales_p = next((p for p in perspectives if p.domain == "sales"), None)
        mkt_p = next((p for p in perspectives if p.domain == "marketing"), None)
        ops_p = next((p for p in perspectives if p.domain == "operations"), None)

        if risk_score >= 50:
            debate_points.append(
                AgentDebatePoint(
                    topic="Capital Allocation: Aggressive Growth vs Expense Containment",
                    advocating_agents=["Sales Intelligence Agent", "Marketing Intelligence Agent"],
                    dissenting_agents=["Finance Intelligence Agent", "Risk & Compliance Agent"],
                    tension_description=(
                        f"Commercial agents seek budget expansion to capture market share, but business risk is {risk_data.get('risk_level')} ({risk_score}/100) with elevated expense ratios."
                    ),
                    resolution=(
                        "Implement milestone-gated spending: cap fixed marketing commitments and condition sales expansion on verified positive contribution margin."
                    ),
                )
            )

        # 2. Pricing & Customer Monetization Tradeoff
        if sales_p and sales_p.sentiment in {"Cautious", "Critical"}:
            debate_points.append(
                AgentDebatePoint(
                    topic="Commercial Strategy: Volume Discounting vs Margin Expansion",
                    advocating_agents=["Sales Intelligence Agent"],
                    dissenting_agents=["Finance Intelligence Agent"],
                    tension_description=(
                        "Sales indicates low ARPU and pressure to close deals, while Finance requires margin preservation to prevent operational losses."
                    ),
                    resolution=(
                        "Maintain floor pricing with value-add service add-ons rather than direct discounts, protecting gross margins."
                    ),
                )
            )

        # 3. Headcount Scaling vs Efficiency
        if ops_p and ops_p.sentiment in {"Cautious", "Critical"} and fin_p and fin_p.sentiment != "Bullish":
            debate_points.append(
                AgentDebatePoint(
                    topic="Workforce Optimization: Capacity Expansion vs Productivity Enhancement",
                    advocating_agents=["Operations & Strategy Agent"],
                    dissenting_agents=["Finance Intelligence Agent", "Risk & Compliance Agent"],
                    tension_description=(
                        "Workforce revenue leverage is compressed while payroll represents a large fixed cost driver."
                    ),
                    resolution=(
                        "Freeze net new headcount additions for 90 days while deploying AI automation to elevate team throughput."
                    ),
                )
            )

        if not debate_points:
            debate_points.append(
                AgentDebatePoint(
                    topic="Strategic Alignment: Scaling Operating Leverage",
                    advocating_agents=["Finance Intelligence Agent", "Sales Intelligence Agent", "Marketing Intelligence Agent"],
                    dissenting_agents=[],
                    tension_description="All agents are aligned on healthy fundamentals with low structural friction.",
                    resolution="Accelerate scalable product-led growth initiatives while maintaining current expense disciplines.",
                )
            )

        return debate_points

    def _generate_explainable_recommendations(
        self,
        perspectives: List[AgentPerspective],
        risk_data: Dict[str, Any],
        debate_points: List[AgentDebatePoint],
    ) -> List[ExplainableRecommendation]:
        recs: List[ExplainableRecommendation] = []
        risk_score = risk_data.get("risk_score", 0)

        # Recommendation 1: Risk & Cost Action
        if risk_score > 30:
            recs.append(
                ExplainableRecommendation(
                    id="REC-OPT-01",
                    title="Implement Operating Expense Optimization & Procurement Review",
                    category="Cost Optimization",
                    priority="High" if risk_score < 70 else "Critical",
                    action_plan=[
                        "Audit recurring software subscriptions and vendor contracts exceeding $5,000.",
                        "Consolidate operational tooling and negotiate 10-15% volume discounts.",
                        "Establish weekly cash burn and budget-vs-actual variance tracking.",
                    ],
                    rationale=(
                        f"Expense ratio is at {risk_data.get('expense_ratio', 0):.1f}%, driving risk score to {risk_score}/100. "
                        "Containment directly protects business runway."
                    ),
                    evidence_metrics={
                        "risk_score": risk_score,
                        "expense_ratio": risk_data.get("expense_ratio", 0),
                        "profit_margin": risk_data.get("profit_margin", 0),
                    },
                    expected_impact="Reduces monthly operational burn by 8-12% and improves net margins.",
                    quantified_roi_estimate="Estimated $15,000-$35,000 annualized expense savings",
                    risk_reduction_potential=min(25, max(10, risk_score // 3)),
                    timeframe="Immediate (0-30 days)",
                    feasibility_score=85,
                )
            )

        # Recommendation 2: Sales & Revenue Monetization
        sales_p = next((p for p in perspectives if p.domain == "sales"), None)
        arpu = sales_p.metrics.get("revenue_per_customer", 0) if sales_p else 0
        recs.append(
            ExplainableRecommendation(
                id="REC-REV-02",
                title="Deploy Account Expansion & Tiered Pricing Architecture",
                category="Revenue Scaling",
                priority="High" if arpu < 300 else "Medium",
                action_plan=[
                    "Analyze usage cohorts among top 20% of customers to package premium features.",
                    "Introduce tiered annual commitment plans with upfront cash collection incentives.",
                    "Institute dedicated customer success checkpoints at 30, 60, and 90 days to drive retention.",
                ],
                rationale=(
                    f"Current ARPU is ${arpu:,.2f}. Improving expansion revenue yields 4x greater capital efficiency than cold acquisition."
                ),
                evidence_metrics={
                    "revenue_per_customer": arpu,
                    "customer_count": sales_p.metrics.get("customers", 0) if sales_p else 0,
                },
                expected_impact="Elevates average contract value by 15-20% and accelerates cash inflow.",
                quantified_roi_estimate="Projected +12-18% top-line revenue expansion within 2 quarters",
                risk_reduction_potential=15,
                timeframe="Short-Term (30-90 days)",
                feasibility_score=80,
            )
        )

        # Recommendation 3: Operational Efficiency
        ops_p = next((p for p in perspectives if p.domain == "operations"), None)
        rev_emp = ops_p.metrics.get("revenue_per_employee", 0) if ops_p else 0
        recs.append(
            ExplainableRecommendation(
                id="REC-OPS-03",
                title="Integrate AI Automation in Core Operational Workflows",
                category="Operational Leverage",
                priority="Medium",
                action_plan=[
                    "Deploy automated reporting for finance and executive leadership.",
                    "Automate customer onboarding workflows to shorten time-to-value.",
                    "Establish standardized KPI dashboards across sales, marketing, and engineering.",
                ],
                rationale=(
                    f"Workforce leverage is ${rev_emp:,.2f} per employee. Automated tooling expands output without requiring headcount growth."
                ),
                evidence_metrics={
                    "revenue_per_employee": rev_emp,
                    "headcount": ops_p.metrics.get("employees", 0) if ops_p else 0,
                },
                expected_impact="Increases throughput per employee by 25% without adding payroll overhead.",
                quantified_roi_estimate="Saves approximately 15 hours per team member monthly",
                risk_reduction_potential=10,
                timeframe="Short-Term (30-90 days)",
                feasibility_score=90,
            )
        )

        return recs

    def synthesize(self, request: MultiAgentSynthesisRequest) -> MultiAgentSynthesisResponse:
        """
        Coordinate all specialized domain agents, perform debate synthesis,
        calculate consensus metrics, and return actionable strategic intelligence.
        """
        data = request.business_data

        # 1. Run domain agent analyses
        fin_p = self._analyze_finance(data)
        sales_p = self._analyze_sales(data)
        mkt_p = self._analyze_marketing(data)
        risk_p, risk_data = self._analyze_risk(data)
        ops_p = self._analyze_operations(data)

        perspectives = [fin_p, sales_p, mkt_p, risk_p, ops_p]

        # 2. Conduct cross-agent debate and identify friction points
        debate_points = self._conduct_debate(perspectives, risk_data)

        # 3. Compute quantitative consensus score (0-100%)
        # Base consensus: 100 minus penalty for sentiment divergence and debate friction
        sentiment_weights = {"Bullish": 1.0, "Neutral": 0.8, "Cautious": 0.5, "Critical": 0.2}
        avg_sentiment = sum(sentiment_weights.get(p.sentiment, 0.5) for p in perspectives) / len(perspectives)
        friction_penalty = len([d for d in debate_points if d.dissenting_agents]) * 12
        consensus_score = max(20, min(100, int(avg_sentiment * 100 - friction_penalty)))

        if consensus_score >= 75:
            consensus_status = "High Alignment"
        elif consensus_score >= 50:
            consensus_status = "Moderate Alignment"
        else:
            consensus_status = "Strategic Tension Detected"

        # 4. Generate explainable recommendations
        recs = self._generate_explainable_recommendations(perspectives, risk_data, debate_points)

        # 5. Synthesize unified executive plan
        risk_level = risk_data.get("risk_level", "Medium")
        executive_plan = (
            f"The multi-agent system assessed the business with a consensus score of {consensus_score}% ({consensus_status}). "
            f"Business risk is classified as {risk_level} ({risk_data.get('risk_score', 0)}/100). "
            f"Top priority is {recs[0].title.lower()}, backed by consensus among Finance and Risk agents to preserve capital while "
            f"guiding Sales toward higher customer monetization."
        )

        return MultiAgentSynthesisResponse(
            consensus_score=consensus_score,
            consensus_status=consensus_status,
            perspectives=perspectives,
            debate_points=debate_points,
            risk_assessment=risk_data,
            executive_consensus_plan=executive_plan,
            prioritized_recommendations=recs,
        )
