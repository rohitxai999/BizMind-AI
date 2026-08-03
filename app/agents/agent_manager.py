from typing import Dict

from app.agents.base_agent import BaseAgent


class AgentManager:
    """
    Registers and manages all BizMind AI agents.
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.name] = agent

    def get_agent(self, name: str):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())

    def analyze(self, agent_name: str, data):
        agent = self.get_agent(agent_name)

        if agent is None:
            raise ValueError(f"Agent '{agent_name}' not found.")

        return agent.analyze(data)