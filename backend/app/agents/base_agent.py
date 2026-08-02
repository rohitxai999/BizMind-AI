from abc import ABC, abstractmethod
from datetime import datetime


class BaseAgent(ABC):
    """
    Base class for all BizMind AI agents.
    """

    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()

    @abstractmethod
    def analyze(self, data: dict):
        """
        Every agent must implement this method.
        """
        pass

    def metadata(self):
        return {
            "agent_name": self.name,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }