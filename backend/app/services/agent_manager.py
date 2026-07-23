from app.agents.business_agent import BusinessAgent
from app.agents.market_agent import MarketAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.strategy_agent import StrategyAgent


class AgentManager:
    def __init__(self):
        self.business_agent = BusinessAgent()
        self.market_agent = MarketAgent()
        self.finance_agent = FinanceAgent()
        self.strategy_agent = StrategyAgent()

    def analyze_business(self, idea: str):

        try:
            print("Running Business Agent...")
            business_report = self.business_agent.analyze(idea)

            print("Running Market Agent...")
            market_report = self.market_agent.analyze(idea)

            print("Running Finance Agent...")
            finance_report = self.finance_agent.analyze(idea)

            print("Running Strategy Agent...")
            strategy_report = self.strategy_agent.analyze(idea)

            final_report = f"""
# 📊 BizMind AI Business Analysis Report

---

## 🏢 Business Analysis

{business_report}

---

## 📈 Market Research

{market_report}

---

## 💰 Financial Analysis

{finance_report}

---

## 🚀 Strategy Plan

{strategy_report}

"""

            return final_report

        except Exception as e:
            return f"❌ BizMind AI Error: {str(e)}"