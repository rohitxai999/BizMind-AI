from fastapi import FastAPI

from app.routes.dashboard import router as dashboard_router

from utils.data_loader import DataLoader
from agents.analytics_agent import AnalyticsAgent
from agents.business_agent import BusinessAgent
from agents.strategy_agent import StrategyAgent


app = FastAPI(
    title="BizMind AI",
    version="1.0.0",
    description="AI Powered Business Intelligence Platform"
)


# Register Routes
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to BizMind AI",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "BizMind AI Backend"
    }


# Temporary AI Report Test Endpoint
@app.get("/business-report")
def business_report():

    loader = DataLoader()

    data = loader.load_business_data(
        "data/business_data.csv"
    )

    analytics = AnalyticsAgent()
    business = BusinessAgent()
    strategy = StrategyAgent()


    metrics = analytics.analyze(data)

    report = business.analyze_business(metrics)

    advice = strategy.generate_strategy(report)


    return {
        "analytics": metrics,
        "business_analysis": report,
        "strategy": advice
    }