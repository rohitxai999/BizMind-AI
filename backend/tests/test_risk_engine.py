import math

import pytest

from app.services.risk.engine import RiskEngine


def test_risk_findings_include_explanations_and_mitigations():
    result = RiskEngine.calculate(
        {
            "revenue": 100000,
            "expenses": 90000,
            "profit": -10000,
            "revenue_growth": -5,
        }
    )

    assert result["risk_findings"]
    assert result["mitigation_recommendations"]

    for finding in result["risk_findings"]:
        assert finding["factor"]
        assert "observed_value" in finding
        assert finding["threshold"]
        assert finding["severity"]
        assert finding["explanation"]
        assert finding["mitigation"]


def test_zero_revenue_returns_data_quality_warning():
    result = RiskEngine.calculate(
        {
            "revenue": 0,
            "expenses": 0,
            "revenue_growth": 0,
        }
    )

    assert result["data_quality_warnings"]
    assert result["risk_score"] >= 0
    assert result["risk_level"]


def test_existing_response_fields_are_preserved():
    result = RiskEngine.calculate(
        {
            "revenue": 100000,
            "expenses": 40000,
            "profit": 60000,
            "revenue_growth": 20,
        }
    )

    expected_fields = {
        "risk_score",
        "risk_level",
        "risk_factors",
        "risk_explanation",
        "profit_margin",
        "expense_ratio",
        "revenue_growth",
    }

    assert expected_fields.issubset(result.keys())


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("revenue", math.nan),
        ("revenue", math.inf),
        ("expenses", -1),
        ("revenue", True),
        ("profit", math.nan),
        ("revenue_growth", math.inf),
    ],
)
def test_invalid_risk_inputs_are_rejected(field, value):
    data = {
        "revenue": 100000,
        "expenses": 40000,
        "profit": 60000,
        "revenue_growth": 20,
    }
    data[field] = value

    with pytest.raises(ValueError):
        RiskEngine.calculate(data)