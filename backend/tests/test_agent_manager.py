from pprint import pprint

from agents.manager import AgentManager

manager = AgentManager()

sample_data = {
    "revenue": 250000,
    "expenses": 175000,
    "sales": 92,
    "sales_target": 100,
    "campaigns": 5,
    "leads": 75,
    "debt": 50000,
    "cash": 100000
}

result = manager.analyze(sample_data)

pprint(result)