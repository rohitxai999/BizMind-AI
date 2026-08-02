from agents.risk.agent import RiskAgent

agent = RiskAgent()

sample_data = {
    "debt": 50000,
    "cash": 100000
}

result = agent.analyze(sample_data)

print(result)