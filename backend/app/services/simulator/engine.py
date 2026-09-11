from typing import Any, Dict, List, Optional
from app.services.risk.engine import RiskEngine
from app.schemas.scenario import (
    BaselineBusinessInput,
    ProjectedFinancials,
    ScenarioComparisonResponse,
    ScenarioLevers,
    ScenarioResult,
)


class ScenarioSimulatorEngine:
    """
    BizMind AI Business Scenario Simulator Engine.

    Empowers leadership to model what-if scenarios, conduct sensitivity
    analysis, perform stress testing, and quantify risk/profit tradeoffs
    using centralized RiskEngine intelligence.
    """

    @staticmethod
    def _compute_financials(
        revenue: float,
        expenses: float,
        customers: int = 0,
        employees: int = 0,
        previous_revenue: float = 0.0,
    ) -> ProjectedFinancials:
        """Calculate standardized financial KPIs from inputs."""
        revenue = max(0.0, float(revenue))
        expenses = max(0.0, float(expenses))
        customers = max(0, int(customers))
        employees = max(0, int(employees))
        previous_revenue = max(0.0, float(previous_revenue))

        profit = revenue - expenses
        profit_margin = (profit / revenue * 100.0) if revenue > 0 else 0.0
        expense_ratio = (expenses / revenue * 100.0) if revenue > 0 else (100.0 if expenses > 0 else 0.0)
        revenue_growth = (
            ((revenue - previous_revenue) / previous_revenue * 100.0)
            if previous_revenue > 0
            else 0.0
        )
        customer_value = (revenue / customers) if customers > 0 else 0.0
        revenue_per_employee = (revenue / employees) if employees > 0 else 0.0

        return ProjectedFinancials(
            revenue=round(revenue, 2),
            expenses=round(expenses, 2),
            profit=round(profit, 2),
            profit_margin=round(profit_margin, 2),
            expense_ratio=round(expense_ratio, 2),
            revenue_growth=round(revenue_growth, 2),
            customer_value=round(customer_value, 2),
            revenue_per_employee=round(revenue_per_employee, 2),
            customers=customers,
            employees=employees,
        )

    @staticmethod
    def _compute_health_score(financials: ProjectedFinancials) -> int:
        """Compute standardized business health score (0-100)."""
        score = 100

        if financials.profit_margin < 10:
            score -= 30
        elif financials.profit_margin < 15:
            score -= 20
        elif financials.profit_margin < 20:
            score -= 10

        if financials.expense_ratio > 80:
            score -= 25
        elif financials.expense_ratio > 70:
            score -= 15
        elif financials.expense_ratio > 60:
            score -= 10

        if financials.revenue_growth < 0:
            score -= 25
        elif financials.revenue_growth < 10:
            score -= 10

        if financials.customers > 0 and financials.customer_value < 100:
            score -= 10

        return max(0, min(100, score))

    @staticmethod
    def get_preset_scenarios() -> List[ScenarioLevers]:
        """Return library of standard industry stress tests and growth scenarios."""
        return [
            ScenarioLevers(
                scenario_name="Aggressive Expansion",
                revenue_change_pct=25.0,
                expense_change_pct=18.0,
                customer_change_pct=20.0,
                employee_change=3,
                description="Invest heavily into growth channels and hire staff to scale revenue.",
            ),
            ScenarioLevers(
                scenario_name="Cost Optimization",
                revenue_change_pct=0.0,
                expense_change_pct=-15.0,
                customer_change_pct=0.0,
                employee_change=0,
                description="Streamline operational overhead without sacrificing existing customer volume.",
            ),
            ScenarioLevers(
                scenario_name="Recession Stress Test",
                revenue_change_pct=-20.0,
                expense_change_pct=5.0,
                customer_change_pct=-15.0,
                employee_change=0,
                description="Downside shock testing vulnerability to demand contraction and inflationary costs.",
            ),
            ScenarioLevers(
                scenario_name="Pricing Power & Margin Expansion",
                revenue_change_pct=10.0,
                expense_change_pct=0.0,
                customer_change_pct=-2.0,
                employee_change=0,
                description="Increase pricing with minimal customer churn to directly expand gross margins.",
            ),
            ScenarioLevers(
                scenario_name="Severe Supply / Cost Shock",
                revenue_change_pct=-10.0,
                expense_change_pct=15.0,
                customer_change_pct=-5.0,
                employee_change=0,
                description="Simulate input cost surges accompanied by top-line softening.",
            ),
        ]

    def simulate(
        self,
        baseline: BaselineBusinessInput,
        scenario: ScenarioLevers,
    ) -> ScenarioResult:
        """
        Execute a single what-if business simulation against baseline metrics.
        """
        # 1. Evaluate baseline state
        baseline_financials = self._compute_financials(
            revenue=baseline.revenue,
            expenses=baseline.expenses,
            customers=baseline.customers,
            employees=baseline.employees,
            previous_revenue=baseline.previous_revenue,
        )

        baseline_risk_eval = RiskEngine.calculate(
            {
                "revenue": baseline_financials.revenue,
                "expenses": baseline_financials.expenses,
                "profit": baseline_financials.profit,
                "revenue_growth": baseline_financials.revenue_growth,
            }
        )
        baseline_risk_score = baseline_risk_eval["risk_score"]
        baseline_risk_level = baseline_risk_eval["risk_level"]
        baseline_health = self._compute_health_score(baseline_financials)

        # 2. Project levers onto baseline
        proj_rev = baseline.revenue * (1.0 + scenario.revenue_change_pct / 100.0)
        proj_exp = baseline.expenses * (1.0 + scenario.expense_change_pct / 100.0)
        proj_cust = int(
            round(baseline.customers * (1.0 + scenario.customer_change_pct / 100.0))
        )
        proj_emp = max(0, baseline.employees + scenario.employee_change)

        projected_financials = self._compute_financials(
            revenue=proj_rev,
            expenses=proj_exp,
            customers=proj_cust,
            employees=proj_emp,
            previous_revenue=baseline.revenue,  # growth measured vs current baseline
        )

        # 3. Evaluate projected risk & health using centralized RiskEngine
        projected_risk_eval = RiskEngine.calculate(
            {
                "revenue": projected_financials.revenue,
                "expenses": projected_financials.expenses,
                "profit": projected_financials.profit,
                "revenue_growth": projected_financials.revenue_growth,
            }
        )
        projected_risk_score = projected_risk_eval["risk_score"]
        projected_risk_level = projected_risk_eval["risk_level"]
        projected_health = self._compute_health_score(projected_financials)

        # 4. Compute deltas & trajectories
        risk_delta = projected_risk_score - baseline_risk_score
        health_delta = projected_health - baseline_health
        profit_delta = projected_financials.profit - baseline_financials.profit

        if risk_delta <= -5:
            risk_trajectory = "IMPROVED"
        elif risk_delta >= 5:
            risk_trajectory = "DETERIORATED"
        else:
            risk_trajectory = "NEUTRAL"

        # 5. Strategic feasibility grading
        if projected_financials.profit < 0:
            strategic_feasibility = "CRITICAL_DOWNSIDE"
        elif projected_risk_level in {"High", "Critical"} or risk_delta >= 25:
            strategic_feasibility = "HIGH_RISK_CAUTION"
        elif profit_delta > 0 and risk_delta <= 0:
            strategic_feasibility = "HIGHLY_RECOMMENDED"
        elif profit_delta > 0 and projected_risk_level in {"Low", "Medium"}:
            strategic_feasibility = "VIABLE_WITH_MONITORING"
        elif profit_delta < 0 and risk_delta <= 0:
            strategic_feasibility = "DEFENSIVE_STABILIZATION"
        else:
            strategic_feasibility = "HIGH_RISK_CAUTION"

        # 6. Synthesize executive impact summary and takeaways
        summary = (
            f"Scenario '{scenario.scenario_name}': Projected profit moves by "
            f"{'+' if profit_delta >= 0 else ''}{profit_delta:,.2f} "
            f"(to {projected_financials.profit:,.2f}), with profit margin of {projected_financials.profit_margin}%. "
            f"Risk score changes by {'+' if risk_delta >= 0 else ''}{risk_delta} pts "
            f"resulting in a {projected_risk_level} risk profile (health score: {projected_health}/100)."
        )

        takeaways = []
        if profit_delta > 0:
            takeaways.append(
                f"Boosts net profit by ${profit_delta:,.2f} relative to current baseline."
            )
        else:
            takeaways.append(
                f"Reduces net profit by ${abs(profit_delta):,.2f} under simulated conditions."
            )

        if risk_trajectory == "IMPROVED":
            takeaways.append(
                f"Improves business resilience by cutting risk score from {baseline_risk_score} to {projected_risk_score}."
            )
        elif risk_trajectory == "DETERIORATED":
            takeaways.append(
                f"Elevates vulnerability; risk score increases from {baseline_risk_score} to {projected_risk_score} ({projected_risk_level})."
            )
        else:
            takeaways.append(
                f"Maintains risk stability at {projected_risk_level} (score: {projected_risk_score})."
            )

        if projected_financials.expense_ratio > 70:
            takeaways.append(
                f"Operating expenses consume {projected_financials.expense_ratio}% of top-line revenue."
            )

        if projected_financials.revenue_per_employee > baseline_financials.revenue_per_employee:
            takeaways.append(
                f"Headcount efficiency rises to ${projected_financials.revenue_per_employee:,.2f} per employee."
            )

        return ScenarioResult(
            scenario_name=scenario.scenario_name,
            description=scenario.description,
            baseline_financials=baseline_financials,
            projected_financials=projected_financials,
            baseline_risk_score=baseline_risk_score,
            baseline_risk_level=baseline_risk_level,
            projected_risk_score=projected_risk_score,
            projected_risk_level=projected_risk_level,
            risk_delta=risk_delta,
            risk_trajectory=risk_trajectory,
            baseline_health_score=baseline_health,
            projected_health_score=projected_health,
            health_delta=health_delta,
            strategic_feasibility=strategic_feasibility,
            executive_impact_summary=summary,
            key_takeaways=takeaways,
        )

    def compare_scenarios(
        self,
        baseline: BaselineBusinessInput,
        scenarios: Optional[List[ScenarioLevers]] = None,
    ) -> ScenarioComparisonResponse:
        """
        Compare multiple what-if scenarios side-by-side, determine optimal path,
        and generate strategic executive guidance.
        """
        if not scenarios:
            scenarios = self.get_preset_scenarios()

        results: List[ScenarioResult] = [
            self.simulate(baseline, sc) for sc in scenarios
        ]

        baseline_financials = self._compute_financials(
            revenue=baseline.revenue,
            expenses=baseline.expenses,
            customers=baseline.customers,
            employees=baseline.employees,
            previous_revenue=baseline.previous_revenue,
        )

        # Determine best options
        highest_profit_res = max(
            results, key=lambda r: r.projected_financials.profit
        )
        lowest_risk_res = min(
            results, key=lambda r: r.projected_risk_score
        )

        # Recommended: maximize profit among non-critical risk options
        viable = [
            r
            for r in results
            if r.projected_risk_level in {"Low", "Medium"}
            and r.projected_financials.profit > 0
        ]
        if viable:
            recommended_res = max(
                viable, key=lambda r: r.projected_financials.profit
            )
        else:
            # Fallback to least risky
            recommended_res = lowest_risk_res

        guidance = (
            f"Based on comparative simulation across {len(results)} scenarios, "
            f"'{recommended_res.scenario_name}' is recommended for strategic execution. "
            f"It delivers ${recommended_res.projected_financials.profit:,.2f} in profit "
            f"with a {recommended_res.projected_risk_level} risk profile (score {recommended_res.projected_risk_score}/100). "
            f"For maximum capital preservation, '{lowest_risk_res.scenario_name}' offers the lowest risk score ({lowest_risk_res.projected_risk_score})."
        )

        return ScenarioComparisonResponse(
            baseline_financials=baseline_financials,
            total_scenarios=len(results),
            results=results,
            recommended_scenario=recommended_res.scenario_name,
            highest_profit_scenario=highest_profit_res.scenario_name,
            lowest_risk_scenario=lowest_risk_res.scenario_name,
            executive_guidance=guidance,
        )

    def run_stress_test(
        self, baseline: BaselineBusinessInput
    ) -> ScenarioComparisonResponse:
        """Run downside stress test scenarios (Recession and Cost Shock)."""
        presets = self.get_preset_scenarios()
        stress_scenarios = [
            s
            for s in presets
            if "Stress" in s.scenario_name or "Shock" in s.scenario_name
        ]
        return self.compare_scenarios(baseline, stress_scenarios)
