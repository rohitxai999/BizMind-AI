from fastapi import APIRouter, UploadFile, File
import os

from app.agents.data_agent import DataAnalystAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.strategy_agent import StrategyAgent
from app.agents.health_agent import HealthAgent


router = APIRouter()


data_agent = DataAnalystAgent()
finance_agent = FinanceAgent()
strategy_agent = StrategyAgent()
health_agent = HealthAgent()


# -----------------------------
# Data Analysis Agent API
# -----------------------------

@router.post("/analyze")
async def analyze_business(file: UploadFile = File(...)):

    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = data_agent.analyze(file_path)

    return result


# -----------------------------
# Finance Agent API
# -----------------------------

@router.post("/finance")
async def finance_analysis(file: UploadFile = File(...)):

    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = finance_agent.analyze(file_path)

    return result


# -----------------------------
# Strategy Agent API
# -----------------------------

@router.post("/strategy")
async def create_strategy(data: dict):

    result = strategy_agent.generate_strategy(
        data["revenue"],
        data["profit"],
        data["risk"]
    )

    return result


# -----------------------------
# Business Health Agent API
# -----------------------------

@router.post("/health")
async def business_health(data: dict):

    result = health_agent.calculate(
        data["revenue"],
        data["profit"],
        data["expenses"],
        data["risk"]
    )

    return result