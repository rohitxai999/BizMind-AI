from agents.finance.agent import FinanceAgent

agent = FinanceAgent()

sample_data = {
    "revenue": 250000,
    "expenses": 175000
}

result = agent.analyze(sample_data)

print(result)