from agents.sales.agent import SalesAgent

agent = SalesAgent()

sample_data = {
    "sales": 92,
    "sales_target": 100
}

result = agent.analyze(sample_data)

print(result)