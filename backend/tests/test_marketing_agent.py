from agents.marketing.agent import MarketingAgent

agent = MarketingAgent()

sample_data = {
    "campaigns": 5,
    "leads": 75
}

result = agent.analyze(sample_data)

print(result)