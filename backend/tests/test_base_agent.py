from app.agents.base_agent import BaseAgent


class DemoAgent(BaseAgent):

    def __init__(self):
        super().__init__("Demo Agent")

    def analyze(self, data):
        return {
            "message": "BaseAgent is working!",
            "input": data,
        }


def test_base_agent():
    agent = DemoAgent()

    metadata = agent.metadata()
    result = agent.analyze({"value": 100})

    assert metadata is not None
    assert result["message"] == "BaseAgent is working!"
    assert result["input"]["value"] == 100