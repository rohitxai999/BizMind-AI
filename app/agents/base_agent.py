from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all BizMind AI agents.
    Every agent should inherit from this class.
    """

    def __init__(self, name: str):
        self.name = name
        self.status = "Ready"

    @abstractmethod
    def analyze(self, data):
        """
        Each agent must implement its own analysis logic.
        """
        pass

    def get_info(self):
        return {
            "agent_name": self.name,
            "status": self.status
        }