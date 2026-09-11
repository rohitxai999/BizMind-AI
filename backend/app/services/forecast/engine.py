import math
from typing import List, Tuple
import numpy as np

from app.schemas.forecast import (
    ForecastedDataPoint,
    ForecastRequest,
    ForecastResponse,
    HistoricalDataPoint,
    TrendAnalysis,
)
from app.services.risk.engine import RiskEngine


class ForecastEngine:
    """
    BizMind AI Predictive Analytics & Time-Series Forecasting Engine.

    Combines linear regression, exponential trend smoothing, prediction
    intervals, anomaly detection, and forward risk trajectory evaluation
    via RiskEngine.
    """

    Z_SCORES = {
        0.80: 1.282,
        0.85: 1.440,
        0.90: 1.645,
        0.95: 1.960,
        0.99: 2.576,
    }

    @staticmethod
    def _get_z_multiplier(confidence_level: float) -> float:
        """Map confidence level to standard normal z-multiplier."""
        # Find closest defined z-score
        closest_conf = min(
            ForecastEngine.Z_SCORES.keys(),
            key=lambda c: abs(c - confidence_level),
        )
        return ForecastEngine.Z_SCORES[closest_conf]

    @staticmethod
    def _fit_trend(y_series: np.ndarray) -> Tuple[float, float, float]:
        """
        Fit linear trend line to series and calculate residual standard error.
        Returns: (slope, intercept, residual_standard_error)
        """
        n = len(y_series)
        x = np.arange(n, dtype=float)

        if n <= 1:
            return 0.0, float(y_series[0]) if n == 1 else 0.0, 0.0

        # Linear regression least-squares fit
        x_mean = np.mean(x)
        y_mean = np.mean(y_series)

        numerator = np.sum((x - x_mean) * (y_series - y_mean))
        denominator = np.sum((x - x_mean) ** 2)

        slope = numerator / denominator if denominator != 0 else 0.0
        intercept = y_mean - slope * x_mean

        # Residuals
        fitted = slope * x + intercept
        residuals = y_series - fitted
        degrees_of_freedom = max(1, n - 2)
        residual_std_error = float(
            np.sqrt(np.sum(residuals**2) / degrees_of_freedom)
        )

        return float(slope), float(intercept), residual_std_error

    @staticmethod
    def _detect_anomalies(
        periods: List[str], values: np.ndarray, metric_name: str
    ) -> List[str]:
        """Flag historical values with |Z-score| > 2.0 as statistical outliers."""
        n = len(values)
        if n < 4:
            return []

        mean = np.mean(values)
        std = np.std(values)
        if std == 0:
            return []

        anomalies = []
        for period, val in zip(periods, values):
            z = (val - mean) / std
            if abs(z) >= 2.0:
                direction = "high" if z > 0 else "low"
                anomalies.append(
                    f"{period}: Unusually {direction} {metric_name} (${val:,.2f}, z-score: {z:+.2f})."
                )
        return anomalies

    @staticmethod
    def _generate_next_period_label(last_period: str, step: int) -> str:
        """Generate intuitive label for future periods."""
        # If period looks like "2026-01"
        if "-" in last_period and len(last_period.split("-")) == 2:
            parts = last_period.split("-")
            try:
                year = int(parts[0])
                month = int(parts[1])
                total_months = month + step
                new_year = year + (total_months - 1) // 12
                new_month = ((total_months - 1) % 12) + 1
                return f"{new_year}-{new_month:02d}"
            except ValueError:
                pass

        # If period contains 'Month X' or 'Period X'
        for prefix in ["Month ", "Period ", "M", "Q"]:
            if last_period.startswith(prefix):
                num_part = last_period[len(prefix) :].strip()
                try:
                    num = int(num_part)
                    return f"{prefix}{num + step}"
                except ValueError:
                    pass

        return f"{last_period} +{step}"

    def predict(self, request: ForecastRequest) -> ForecastResponse:
        """
        Generate forward predictive forecasts for revenue and expenses with
        confidence bands, volatility analytics, and risk assessments.
        """
        historical = request.historical_data
        n = len(historical)

        periods = [h.period for h in historical]
        revenues = np.array([float(h.revenue) for h in historical], dtype=float)
        expenses = np.array([float(h.expenses) for h in historical], dtype=float)

        # 1. Detect historical anomalies if requested
        anomalies = []
        if request.include_anomaly_detection:
            anomalies.extend(
                self._detect_anomalies(periods, revenues, "Revenue")
            )
            anomalies.extend(
                self._detect_anomalies(periods, expenses, "Expenses")
            )

        # 2. Fit trends
        rev_slope, rev_intercept, rev_rse = self._fit_trend(revenues)
        exp_slope, exp_intercept, exp_rse = self._fit_trend(expenses)

        # 3. Growth and volatility metrics
        avg_rev = float(np.mean(revenues)) if np.mean(revenues) > 0 else 1.0
        rev_growth_rates = []
        for i in range(1, n):
            if revenues[i - 1] > 0:
                rev_growth_rates.append(
                    (revenues[i] - revenues[i - 1]) / revenues[i - 1] * 100.0
                )
        avg_period_growth = (
            float(np.mean(rev_growth_rates)) if rev_growth_rates else 0.0
        )

        std_rev = float(np.std(revenues))
        volatility_score = round((std_rev / avg_rev) * 100.0, 2)

        # Trend direction classification
        if rev_slope > avg_rev * 0.05:
            rev_trend_dir = "STRONG_GROWTH"
        elif rev_slope > 0:
            rev_trend_dir = "MODERATE_GROWTH"
        elif rev_slope < -avg_rev * 0.05:
            rev_trend_dir = "RAPID_DECLINE"
        elif rev_slope < 0:
            rev_trend_dir = "MODERATE_DECLINE"
        else:
            rev_trend_dir = "STABLE"

        if exp_slope > rev_slope:
            exp_trend_dir = "EXPANDING_FASTER_THAN_REVENUE"
        elif exp_slope > 0:
            exp_trend_dir = "CONTROLLED_EXPANSION"
        elif exp_slope < 0:
            exp_trend_dir = "CONTRACTING"
        else:
            exp_trend_dir = "STABLE"

        # 4. Generate forecast projections
        z_multiplier = self._get_z_multiplier(request.confidence_level)
        forecasted_points: List[ForecastedDataPoint] = []
        last_period_label = periods[-1]
        baseline_revenue = float(revenues[-1])

        x_mean = (n - 1) / 2.0
        ss_xx = max(1.0, np.sum((np.arange(n) - x_mean) ** 2))

        for h in range(1, request.forecast_periods + 1):
            future_x = (n - 1) + h
            period_label = self._generate_next_period_label(
                last_period_label, h
            )

            # Revenue projection
            pred_rev = max(0.0, rev_slope * future_x + rev_intercept)
            rev_std_h = rev_rse * math.sqrt(
                1.0 + (1.0 / n) + ((future_x - x_mean) ** 2 / ss_xx)
            )
            margin_rev = z_multiplier * rev_std_h
            rev_lower = max(0.0, pred_rev - margin_rev)
            rev_upper = pred_rev + margin_rev

            # Expenses projection
            pred_exp = max(0.0, exp_slope * future_x + exp_intercept)
            exp_std_h = exp_rse * math.sqrt(
                1.0 + (1.0 / n) + ((future_x - x_mean) ** 2 / ss_xx)
            )
            margin_exp = z_multiplier * exp_std_h
            exp_lower = max(0.0, pred_exp - margin_exp)
            exp_upper = pred_exp + margin_exp

            # Projected financials
            pred_profit = pred_rev - pred_exp
            pred_margin = (
                (pred_profit / pred_rev * 100.0) if pred_rev > 0 else 0.0
            )

            # Forward risk evaluation using centralized RiskEngine (Day 14)
            proj_growth = (
                ((pred_rev - baseline_revenue) / baseline_revenue * 100.0)
                if baseline_revenue > 0
                else 0.0
            )
            future_risk_eval = RiskEngine.calculate(
                {
                    "revenue": pred_rev,
                    "expenses": pred_exp,
                    "profit": pred_profit,
                    "revenue_growth": proj_growth,
                }
            )

            forecasted_points.append(
                ForecastedDataPoint(
                    period=period_label,
                    predicted_revenue=round(pred_rev, 2),
                    revenue_lower_bound=round(rev_lower, 2),
                    revenue_upper_bound=round(rev_upper, 2),
                    predicted_expenses=round(pred_exp, 2),
                    expenses_lower_bound=round(exp_lower, 2),
                    expenses_upper_bound=round(exp_upper, 2),
                    predicted_profit=round(pred_profit, 2),
                    projected_profit_margin=round(pred_margin, 2),
                    projected_risk_score=future_risk_eval["risk_score"],
                    projected_risk_level=future_risk_eval["risk_level"],
                )
            )

        # 5. Baseline vs Future Risk Trajectory
        baseline_risk_eval = RiskEngine.calculate(
            {
                "revenue": float(revenues[-1]),
                "expenses": float(expenses[-1]),
                "profit": float(revenues[-1] - expenses[-1]),
                "revenue_growth": avg_period_growth,
            }
        )
        base_risk_score = baseline_risk_eval["risk_score"]
        final_proj_risk_score = forecasted_points[-1].projected_risk_score

        if final_proj_risk_score <= base_risk_score - 5:
            risk_trajectory = "IMPROVING"
        elif final_proj_risk_score >= base_risk_score + 5:
            risk_trajectory = "DETERIORATING"
        else:
            risk_trajectory = "STABLE"

        # 6. Run rate and executive takeaway
        # Standardized annual run rate estimation (projected monthly avg * 12 or period rate)
        latest_predicted_rev = forecasted_points[-1].predicted_revenue
        projected_annual_run_rate = round(latest_predicted_rev * 12.0, 2)

        final_period = forecasted_points[-1]
        executive_takeaway = (
            f"Forecast projects revenue to trend {rev_trend_dir.lower().replace('_', ' ')} "
            f"reaching ${final_period.predicted_revenue:,.2f} by {final_period.period} "
            f"with a profit margin of {final_period.projected_profit_margin}%. "
            f"Risk profile is expected to remain {final_period.projected_risk_level.lower()} "
            f"(projected score {final_period.projected_risk_score}/100, trajectory: {risk_trajectory.lower()})."
        )

        trend_analysis = TrendAnalysis(
            revenue_trend_direction=rev_trend_dir,
            avg_period_growth_rate=round(avg_period_growth, 2),
            expense_trend_direction=exp_trend_dir,
            volatility_score=volatility_score,
            anomalies_detected=anomalies,
        )

        confidence_score = round(
            max(0.60, min(0.98, 1.0 - (volatility_score / 100.0) * 0.4)), 2
        )

        return ForecastResponse(
            forecast_horizon=request.forecast_periods,
            forecasted_periods=forecasted_points,
            trend_analysis=trend_analysis,
            projected_annual_run_rate=projected_annual_run_rate,
            projected_future_risk_trajectory=risk_trajectory,
            executive_takeaway=executive_takeaway,
            confidence_score=confidence_score,
        )

    def get_sample_forecast(self, periods: int = 3) -> ForecastResponse:
        """Convenience method returning forecast from benchmark 6-month historical data."""
        benchmark_history = [
            HistoricalDataPoint(
                period="Month 1", revenue=180000, expenses=115000, customers=120
            ),
            HistoricalDataPoint(
                period="Month 2", revenue=192000, expenses=118000, customers=128
            ),
            HistoricalDataPoint(
                period="Month 3", revenue=205000, expenses=123000, customers=135
            ),
            HistoricalDataPoint(
                period="Month 4", revenue=218000, expenses=129000, customers=144
            ),
            HistoricalDataPoint(
                period="Month 5", revenue=234000, expenses=135000, customers=155
            ),
            HistoricalDataPoint(
                period="Month 6", revenue=250000, expenses=142000, customers=168
            ),
        ]
        request = ForecastRequest(
            historical_data=benchmark_history,
            forecast_periods=periods,
            confidence_level=0.90,
        )
        return self.predict(request)
