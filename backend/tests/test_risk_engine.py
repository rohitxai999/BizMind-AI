from app.services.risk.engine import RiskEngine


def test_low_business_risk():
    result = RiskEngine.calculate(
        {
            "revenue": 100000,
            "expenses": 40000,
            "profit": 60000,
            "revenue_growth": 20,
        }
    )

    assert result["risk_score"] == 0
    assert result["risk_level"] == "Low"


def test_medium_business_risk():
    result = RiskEngine.calculate(
        {
            "revenue": 100000,
            "expenses": 65000,
            "profit": 35000,
            "revenue_growth": 5,
        }
    )

    assert result["risk_score"] == 20
    assert result["risk_level"] == "Low"


def test_high_business_risk():
    result = RiskEngine.calculate(
        {
            "revenue": 100000,
            "expenses": 75000,
            "profit": 25000,
            "revenue_growth": -5,
        }
    )

    assert result["risk_score"] == 40
    assert result["risk_level"] == "Medium"


def test_critical_business_risk():
    result = RiskEngine.calculate(
        {
            "revenue": 100000,
            "expenses": 90000,
            "profit": -10000,
            "revenue_growth": -10,
        }
    )

    assert result["risk_score"] == 90
    assert result["risk_level"] == "Critical"