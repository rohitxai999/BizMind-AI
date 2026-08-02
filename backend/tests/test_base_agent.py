from agents.base_agent import BaseAgent


class DemoAgent(BaseAgent):

    def __init__(self):
        super().__init__("Demo Agent")

    def analyze(self, data):
        return {
            "message": "BaseAgent is working!",
            "input": data
        }


agent = DemoAgent()

print(agent.metadata())
print(agent.analyze({"value": 100}))