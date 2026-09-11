import pytest
from app.schemas.forecast import (
    ForecastRequest,
    HistoricalDataPoint,
)
from app.services.forecast.engine import ForecastEngine


@pytest.fixture
def engine():
    return ForecastEngine()


@pytest.fixture
def growing_history():
    return [
        HistoricalDataPoint(period="Month 1", revenue=100000, expenses=60000),
        HistoricalDataPoint(period="Month 2", revenue=110000, expenses=63000),
        HistoricalDataPoint(period="Month 3", revenue=122000, expenses=67000),
        HistoricalDataPoint(period="Month 4", revenue=135000, expenses=72000),
        HistoricalDataPoint(period="Month 5", revenue=150000, expenses=77000),
    ]


def test_forecast_growing_trend(engine, growing_history):
    req = ForecastRequest(
        historical_data=growing_history,
        forecast_periods=3,
        confidence_level=0.90,
    )
    res = engine.predict(req)

    assert res.forecast_horizon == 3
    assert len(res.forecasted_periods) == 3
    assert res.trend_analysis.revenue_trend_direction in {
        "STRONG_GROWTH",
        "MODERATE_GROWTH",
    }
    assert res.trend_analysis.avg_period_growth_rate > 0

    # Verify prediction bands
    for p in res.forecasted_periods:
        assert p.revenue_upper_bound >= p.predicted_revenue
        assert p.predicted_revenue >= p.revenue_lower_bound
        assert p.expenses_upper_bound >= p.predicted_expenses
        assert p.predicted_expenses >= p.expenses_lower_bound
        assert p.predicted_profit == round(
            p.predicted_revenue - p.predicted_expenses, 2
        )
        assert p.projected_risk_level in {"Low", "Medium", "High", "Critical"}

    assert res.projected_annual_run_rate > 0
    assert res.executive_takeaway != ""


def test_forecast_declining_trend_risk_escalation(engine):
    declining_history = [
        HistoricalDataPoint(period="Q1", revenue=200000, expenses=140000),
        HistoricalDataPoint(period="Q2", revenue=160000, expenses=145000),
        HistoricalDataPoint(period="Q3", revenue=120000, expenses=148000),
        HistoricalDataPoint(period="Q4", revenue=90000, expenses=150000),
    ]
    req = ForecastRequest(
        historical_data=declining_history,
        forecast_periods=2,
    )
    res = engine.predict(req)

    assert "DECLINE" in res.trend_analysis.revenue_trend_direction
    # Risk should deteriorate as expenses exceed declining revenues
    assert res.projected_future_risk_trajectory in {"DETERIORATING", "STABLE"}
    final_period = res.forecasted_periods[-1]
    assert final_period.projected_risk_score >= 30


def test_confidence_interval_width(engine, growing_history):
    req_80 = ForecastRequest(
        historical_data=growing_history,
        forecast_periods=3,
        confidence_level=0.80,
    )
    req_95 = ForecastRequest(
        historical_data=growing_history,
        forecast_periods=3,
        confidence_level=0.95,
    )

    res_80 = engine.predict(req_80)
    res_95 = engine.predict(req_95)

    # 95% confidence interval must be strictly wider than 80%
    width_80 = (
        res_80.forecasted_periods[0].revenue_upper_bound
        - res_80.forecasted_periods[0].revenue_lower_bound
    )
    width_95 = (
        res_95.forecasted_periods[0].revenue_upper_bound
        - res_95.forecasted_periods[0].revenue_lower_bound
    )
    assert width_95 > width_80


def test_anomaly_detection(engine):
    history_with_spike = [
        HistoricalDataPoint(period="2026-01", revenue=100000, expenses=60000),
        HistoricalDataPoint(period="2026-02", revenue=102000, expenses=61000),
        HistoricalDataPoint(period="2026-03", revenue=99000, expenses=59000),
        HistoricalDataPoint(period="2026-04", revenue=101000, expenses=60000),
        HistoricalDataPoint(period="2026-05", revenue=103000, expenses=62000),
        HistoricalDataPoint(
            period="2026-06", revenue=350000, expenses=60000
        ),  # Massive outlier
        HistoricalDataPoint(period="2026-07", revenue=101000, expenses=61000),
    ]
    req = ForecastRequest(
        historical_data=history_with_spike,
        forecast_periods=2,
        include_anomaly_detection=True,
    )
    res = engine.predict(req)

    assert len(res.trend_analysis.anomalies_detected) > 0
    assert any(
        "2026-06" in anom for anom in res.trend_analysis.anomalies_detected
    )


def test_minimum_sparse_data(engine):
    sparse = [
        HistoricalDataPoint(period="2026-01", revenue=100000, expenses=60000),
        HistoricalDataPoint(period="2026-02", revenue=110000, expenses=65000),
    ]
    req = ForecastRequest(
        historical_data=sparse,
        forecast_periods=2,
    )
    res = engine.predict(req)

    assert len(res.forecasted_periods) == 2
    assert res.forecasted_periods[0].predicted_revenue > 0


def test_sample_forecast(engine):
    res = engine.get_sample_forecast(periods=4)
    assert res.forecast_horizon == 4
    assert len(res.forecasted_periods) == 4
    assert res.confidence_score > 0
